"""Endpoints de generación IA de conjuntos AP derivados."""

from __future__ import annotations

import hashlib
import json
import math
import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.ai.modelo_propagacion import ModeloPropagacion, MuestraCalibracionRF
from app.ai.optimizador_ap_service import OptimizadorAPService
from app.api.v1.heatmaps import _conjunto_out, _mapa_out
from app.core.config import settings
from app.core.database import get_db
from app.core.security import require_admin
from app.models.heatmap import ConjuntoAP, MapaCalor
from app.models.inventario_rf import APFisico, BSSIDRadio, RadioAP
from app.models.medicion import MedicionWifi, PuntoMedicion
from app.models.plano import Plano
from app.models.proyecto import Proyecto
from app.models.usuario import Usuario
from app.repositories.heatmap_repository import (
    ConjuntoAPRepository,
    MapaCalorRepository,
)
from app.repositories.medicion_repository import MedicionRepository
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.ia import ConjuntosIAGeneradosOut, RestriccionesIAIn
from app.services.geometria_service import mascara_poligono
from app.services.interpolacion_service import (
    ESCALA_CWNA,
    HeatmapImageService,
    InterpolacionService,
    PuntoRSSI,
)
from app.storage import LocalFilesystemStorage

router_proyectos_escenarios = APIRouter(prefix="/proyectos", tags=["ia"])


def _storage() -> LocalFilesystemStorage:
    return LocalFilesystemStorage(root=settings.storage_root)


def _proyecto_admin(
    *,
    proyecto_id: int,
    current_user: Usuario,
    db: Session,
) -> Proyecto:
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La generación IA está restringida al panel web admin.",
        )
    proyecto = ProyectoRepository(db).obtener_por_id_admin(proyecto_id=proyecto_id)
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return proyecto


def _plano_base(proyecto: Proyecto) -> Plano:
    planos = sorted(proyecto.planos, key=lambda p: p.created_at or p.id, reverse=True)
    plano = next((p for p in planos if p.calibrado), None)
    if plano is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El proyecto requiere al menos un plano calibrado.",
        )
    return plano


def _plano_ia(
    *,
    proyecto: Proyecto,
    plano_id: int | None,
    db: Session,
) -> Plano:
    if plano_id is None:
        return _plano_base(proyecto)
    plano = (
        db.query(Plano)
        .filter(Plano.id == plano_id, Plano.proyecto_id == proyecto.id)
        .first()
    )
    if plano is None:
        raise HTTPException(status_code=404, detail="Plano no encontrado.")
    if not plano.calibrado:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El plano seleccionado debe estar calibrado.",
        )
    return plano


def _conjunto_fuente_entrada(
    *, plano_id: int, body: RestriccionesIAIn, db: Session
) -> ConjuntoAP:
    conjunto = (
        db.query(ConjuntoAP)
        .filter(
            ConjuntoAP.id == body.fuente_entrada.conjunto_id,
            ConjuntoAP.plano_id == plano_id,
        )
        .first()
    )
    if conjunto is None:
        raise HTTPException(
            status_code=422,
            detail="El conjunto seleccionado no pertenece al plano.",
        )
    if conjunto.origen == "ia":
        raise HTTPException(
            status_code=422,
            detail="La IA debe partir de un conjunto técnico, no de una propuesta IA.",
        )
    if not conjunto.items:
        raise HTTPException(
            status_code=422,
            detail="El conjunto seleccionado no contiene APs.",
        )
    return conjunto


def _bssids_conjunto(conjunto: ConjuntoAP) -> list[str]:
    return [item.bssid.lower() for item in conjunto.items]


def _requerir_bssids_medidos(
    *,
    plano: Plano,
    conjunto: ConjuntoAP,
    db: Session,
) -> list[str]:
    solicitados = _bssids_conjunto(conjunto)
    disponibles = {
        ap["bssid"]
        for ap in MedicionRepository(db).listar_aps_por_plano(plano_id=plano.id)
    }
    faltantes = [bssid for bssid in solicitados if bssid not in disponibles]
    if faltantes:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El conjunto contiene APs sin mediciones en el plano.",
        )
    return solicitados


def _limite_aps_derivado(
    *,
    conjunto_fuente: ConjuntoAP | None,
    bssids_seleccionados: list[str] | None,
    aps_existentes: list[dict],
) -> int:
    if conjunto_fuente is not None:
        cantidad_base = len(conjunto_fuente.items)
    elif bssids_seleccionados is not None:
        cantidad_base = len(bssids_seleccionados)
    elif aps_existentes:
        cantidad_base = len(aps_existentes)
    else:
        cantidad_base = 5
    return max(1, min(3, cantidad_base))


def _requerir_poligono_interes(plano: Plano) -> list[dict]:
    poligono = plano.poligono_interes or []
    if len(poligono) < 3:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Debe definir un polígono de interés antes de generar "
                "recomendaciones IA."
            ),
        )
    return poligono


def _mapa_actual(
    *,
    plano: Plano,
    db: Session,
    bssids_seleccionados: list[str],
    conjunto_ap_id: int,
) -> tuple[MapaCalor, list[PuntoRSSI]]:
    mapa_repo = MapaCalorRepository(db)
    med_repo = MedicionRepository(db)
    puntos = med_repo.listar_puntos_rssi_heatmap(
        plano_id=plano.id,
        bssids=bssids_seleccionados,
    )
    if len(puntos) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Se requieren al menos 5 puntos de medición para IA.",
        )
    poligono_interes = _requerir_poligono_interes(plano)
    firma = hashlib.sha1(
        (
            f"ia-actual:{plano.id}:conjunto:{conjunto_ap_id}:"
            f"bssids:{','.join(sorted(set(bssids_seleccionados)))}:"
            f"area:{json.dumps(poligono_interes, sort_keys=True)}:"
            f"{med_repo.firma_mediciones_plano(plano_id=plano.id)}"
        ).encode(),
        usedforsecurity=False,
    ).hexdigest()
    mapa_cache = mapa_repo.obtener_cache(
        plano_id=plano.id,
        algoritmo="IDW",
        resolucion=64,
        firma_mediciones=firma,
    )
    if mapa_cache is not None:
        return mapa_cache, puntos

    matriz = InterpolacionService().interpolar(
        puntos=puntos,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        resolucion=64,
        algoritmo="IDW",
    )
    mascara = mascara_poligono(
        poligono=poligono_interes,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        resolucion=64,
    )
    ruta = f"heatmaps/ia_actual_{plano.id}_{secrets.token_hex(8)}.png"
    _storage().save(HeatmapImageService().render_png(matriz, mascara=mascara), ruta)
    aps = MedicionRepository(db).listar_aps_por_plano(plano_id=plano.id)
    aps_interes = [ap for ap in aps if ap["bssid"] in set(bssids_seleccionados)]
    mapa = mapa_repo.crear(
        plano_id=plano.id,
        conjunto_ap_id=conjunto_ap_id,
        modo_generacion="CONJUNTO_COMPLETO",
        algoritmo="IDW",
        resolucion=64,
        bssid=aps_interes[0]["bssid"],
        ssid=aps_interes[0]["ssid"],
        ap_pos_x=aps_interes[0]["pos_x"],
        ap_pos_y=aps_interes[0]["pos_y"],
        aps_interes=aps_interes,
        bssids_generacion=bssids_seleccionados,
        matriz=matriz,
        escala=ESCALA_CWNA,
        ruta_imagen=ruta,
        cantidad_puntos=len(puntos),
        rssi_min=min(min(fila) for fila in matriz),
        rssi_max=max(max(fila) for fila in matriz),
        firma_mediciones=firma,
    )
    return mapa, puntos


def _modelo_calibrado_para_plano(
    *,
    plano: Plano,
    db: Session,
    bssids_seleccionados: list[str],
) -> ModeloPropagacion:
    query = (
        db.query(MedicionWifi, PuntoMedicion, RadioAP, APFisico)
        .join(PuntoMedicion, MedicionWifi.punto_id == PuntoMedicion.id)
        .join(BSSIDRadio, MedicionWifi.bssid == BSSIDRadio.bssid)
        .join(RadioAP, BSSIDRadio.radio_id == RadioAP.id)
        .join(APFisico, RadioAP.ap_fisico_id == APFisico.id)
        .filter(PuntoMedicion.plano_id == plano.id)
        .filter(APFisico.plano_id == plano.id)
        .filter(RadioAP.habilitada.is_(True))
        .filter(MedicionWifi.bssid.in_(bssids_seleccionados))
    )
    muestras: list[MuestraCalibracionRF] = []
    metros_por_pixel = plano.escala_m_por_px or 1.0
    for medicion, punto, radio, ap in query.all():
        distancia_px = math.hypot(punto.pos_x - ap.coord_x, punto.pos_y - ap.coord_y)
        muestras.append(
            MuestraCalibracionRF(
                distancia_m=max(1.0, distancia_px * metros_por_pixel),
                banda=radio.banda,
                rssi_dbm=float(medicion.rssi),
                potencia_dbm=radio.potencia_dbm,
                ganancia_dbi=radio.ganancia_dbi,
                perdida_cable_db=radio.perdida_cable_db,
            )
        )
    return ModeloPropagacion.calibrar_desde_muestras(muestras)


def _aps_existentes_para_ia(
    *,
    plano_id: int,
    conjunto: ConjuntoAP,
    db: Session,
) -> list[dict]:
    bssids = _bssids_conjunto(conjunto)
    aps = (
        db.query(APFisico)
        .join(RadioAP, RadioAP.ap_fisico_id == APFisico.id)
        .join(BSSIDRadio, BSSIDRadio.radio_id == RadioAP.id)
        .filter(APFisico.plano_id == plano_id)
        .filter(BSSIDRadio.bssid.in_(bssids))
        .distinct()
        .order_by(APFisico.id.asc())
        .all()
    )
    return [
        {
            "id": ap.id,
            "coord_x": ap.coord_x,
            "coord_y": ap.coord_y,
            "altura_m": ap.altura_m,
            "tipo_montaje": ap.tipo_montaje,
            "restriccion_movimiento": ap.restriccion_movimiento,
            "verificado": ap.verificado,
        }
        for ap in aps
    ]


def _nombre_conjunto_ia(
    *,
    repo: ConjuntoAPRepository,
    plano_id: int,
    nombre_base: str,
    indice: int,
) -> str:
    nombre = f"{nombre_base} · IA Propuesta {indice}"
    candidato = nombre
    correlativo = 2
    while repo.existe_nombre(plano_id=plano_id, nombre=candidato):
        candidato = f"{nombre} ({correlativo})"
        correlativo += 1
    return candidato


def _items_conjunto_ia(*, indice: int, recomendaciones: list[dict]) -> list[dict]:
    items: list[dict] = []
    for rec_idx, rec in enumerate(recomendaciones, start=1):
        radio_principal = next(iter(rec.get("radios") or []), {})
        items.append(
            {
                "bssid": f"sp5:{indice:02d}:{rec_idx:02d}:00:00",
                "ssid_snapshot": rec["modelo_ap"],
                "canal_snapshot": radio_principal.get("canal"),
                "rssi_promedio_snapshot": rec["rssi_proyectado"],
                "pos_x": rec["coord_x"],
                "pos_y": rec["coord_y"],
                "accion_recomendada": rec["accion"],
                "justificacion": rec["justificacion"],
                "altura_m": rec["altura_m"],
                "tipo_montaje": rec["tipo_montaje"],
                "banda": rec["banda"],
                "modelo_ap": rec["modelo_ap"],
                "costo_estimado": rec["costo_estimado"],
                "radios": rec["radios"],
            }
        )
    return items


@router_proyectos_escenarios.post(
    "/{proyecto_id}/conjuntos-ap/recomendaciones-ia",
    response_model=ConjuntosIAGeneradosOut,
    status_code=status.HTTP_201_CREATED,
)
def generar_conjuntos_ia(
    proyecto_id: int,
    body: RestriccionesIAIn,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
) -> ConjuntosIAGeneradosOut:
    proyecto = _proyecto_admin(
        proyecto_id=proyecto_id,
        current_user=current_user,
        db=db,
    )
    plano = _plano_ia(proyecto=proyecto, plano_id=body.plano_id, db=db)
    conjunto_fuente = _conjunto_fuente_entrada(plano_id=plano.id, body=body, db=db)
    bssids_seleccionados = _requerir_bssids_medidos(
        plano=plano,
        conjunto=conjunto_fuente,
        db=db,
    )
    mapa_actual, puntos = _mapa_actual(
        plano=plano,
        db=db,
        bssids_seleccionados=bssids_seleccionados,
        conjunto_ap_id=conjunto_fuente.id,
    )
    modelo_propagacion = _modelo_calibrado_para_plano(
        plano=plano,
        db=db,
        bssids_seleccionados=bssids_seleccionados,
    )
    aps_existentes = _aps_existentes_para_ia(
        plano_id=plano.id,
        conjunto=conjunto_fuente,
        db=db,
    )
    limite_aps = _limite_aps_derivado(
        conjunto_fuente=conjunto_fuente,
        bssids_seleccionados=bssids_seleccionados,
        aps_existentes=aps_existentes,
    )
    banda_objetivo = "5" if "5" in body.bandas else body.bandas[0]
    poligono_interes = _requerir_poligono_interes(plano)
    alternativas = OptimizadorAPService(modelo=modelo_propagacion).optimizar(
        puntos_actuales=puntos,
        matriz_actual=mapa_actual.matriz,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        metros_por_pixel=plano.escala_m_por_px or 1.0,
        max_aps=limite_aps,
        banda=banda_objetivo,
        resolucion=body.resolucion,
        umbral_objetivo_dbm=body.umbral_objetivo_dbm,
        bandas=body.bandas,
        aps_existentes=aps_existentes,
        cantidad_recomendaciones=body.cantidad_recomendaciones,
        poligono_interes=poligono_interes,
    )
    conjunto_repo = ConjuntoAPRepository(db)
    mapa_repo = MapaCalorRepository(db)
    conjuntos_ia: list[ConjuntoAP] = []
    mapas_proyectados: list[MapaCalor] = []
    restricciones = body.model_dump(exclude_none=True)
    restricciones["fuente_entrada"]["nombre"] = conjunto_fuente.nombre
    restricciones["fuente_entrada"]["proposito"] = conjunto_fuente.proposito
    restricciones["fuente_entrada"]["bssids"] = bssids_seleccionados
    restricciones["limite_aps_derivado"] = limite_aps
    for idx, alternativa in enumerate(alternativas, start=1):
        items = _items_conjunto_ia(
            indice=idx,
            recomendaciones=alternativa.recomendaciones,
        )
        conjunto_ia = conjunto_repo.crear(
            plano_id=plano.id,
            conjunto_origen_id=conjunto_fuente.id,
            nombre=_nombre_conjunto_ia(
                repo=conjunto_repo,
                plano_id=plano.id,
                nombre_base=conjunto_fuente.nombre,
                indice=idx,
            ),
            proposito=conjunto_fuente.proposito,
            descripcion=conjunto_fuente.descripcion,
            es_principal=False,
            items=items,
            origen="ia",
            creado_por_id=current_user.id,
            resumen_ia=alternativa.resumen,
            metricas_ia={
                **alternativa.metricas,
                "calibracion_modelo": modelo_propagacion.resumen_calibracion(),
                "confianza": alternativa.confianza,
                "supuestos": alternativa.supuestos,
                "mapas_por_banda": alternativa.mapas_por_banda,
            },
            restricciones_ia=restricciones,
            version_motor_ia="rf-hibrido-1.0",
        )
        ruta = f"heatmaps/ia_proyectado_{proyecto.id}_{idx}_{secrets.token_hex(8)}.png"
        _storage().save(
            HeatmapImageService().render_png(
                alternativa.matriz,
                mascara=mascara_poligono(
                    poligono=poligono_interes,
                    ancho_px=plano.ancho_px,
                    alto_px=plano.alto_px,
                    resolucion=body.resolucion,
                ),
            ),
            ruta,
        )
        firma = hashlib.sha1(
            f"ia-proyectado:{proyecto.id}:{conjunto_ia.id}:{secrets.token_hex(8)}".encode(),
            usedforsecurity=False,
        ).hexdigest()
        aps_interes = [
            {
                "bssid": item["bssid"],
                "ssid": item["ssid_snapshot"],
                "canal": item["canal_snapshot"],
                "frecuencia_mhz": None,
                "rssi_promedio": item["rssi_promedio_snapshot"],
                "pos_x": item["pos_x"],
                "pos_y": item["pos_y"],
                "cantidad_puntos": len(puntos),
            }
            for item in items
        ]
        mapa_proyectado = mapa_repo.crear(
            plano_id=plano.id,
            conjunto_ap_id=conjunto_ia.id,
            modo_generacion="PROYECTADO",
            algoritmo="FSPL",
            resolucion=body.resolucion,
            bssid=items[0]["bssid"],
            ssid=conjunto_ia.nombre,
            ap_pos_x=items[0]["pos_x"],
            ap_pos_y=items[0]["pos_y"],
            aps_interes=aps_interes,
            bssids_generacion=[item["bssid"] for item in items],
            matriz=alternativa.matriz,
            escala=ESCALA_CWNA,
            ruta_imagen=ruta,
            cantidad_puntos=len(puntos),
            rssi_min=min(min(fila) for fila in alternativa.matriz),
            rssi_max=max(max(fila) for fila in alternativa.matriz),
            firma_mediciones=firma,
        )
        conjuntos_ia.append(conjunto_ia)
        mapas_proyectados.append(mapa_proyectado)

    return ConjuntosIAGeneradosOut(
        conjunto_base_id=conjunto_fuente.id,
        mapa_actual=_mapa_out(mapa_actual, request),
        conjuntos=[_conjunto_out(conjunto) for conjunto in conjuntos_ia],
        mapas_proyectados=[_mapa_out(mapa, request) for mapa in mapas_proyectados],
    )
