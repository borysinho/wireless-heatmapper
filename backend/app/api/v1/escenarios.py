"""Endpoints de generación IA de conjuntos AP derivados."""

from __future__ import annotations

import hashlib
import json
import math
import secrets
from dataclasses import dataclass
from itertools import combinations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.ai.modelo_propagacion import (
    CorreccionEspacialRF,
    ModeloPropagacion,
    MuestraCalibracionRF,
)
from app.ai.optimizador_ap_service import OptimizadorAPService
from app.api.v1.heatmaps import (
    _conjunto_out,
    _mapa_resumen_out,
    _radio_principal,
    _radio_tx_principal,
)
from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.models.heatmap import ConjuntoAP, MapaCalor
from app.models.medicion import LecturaRSSI, PuntoMedicion
from app.models.plano import Plano
from app.models.proyecto import Proyecto
from app.models.usuario import Usuario
from app.repositories.heatmap_repository import (
    ConjuntoAPRepository,
    MapaCalorRepository,
)
from app.repositories.medicion_repository import (
    ORIGEN_CAMPO,
    ORIGEN_IA_ESTIMADA,
    MedicionRepository,
)
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.ia import ConjuntosIAGeneradosOut, PreparacionIAOut, RestriccionesIAIn
from app.services.geometria_service import mascara_poligono
from app.services.interpolacion_service import (
    ESCALA_CWNA,
    HeatmapImageService,
    InterpolacionService,
    PuntoRSSI,
)
from app.storage import LocalFilesystemStorage

router_proyectos_escenarios = APIRouter(prefix="/proyectos", tags=["ia"])
VERSION_MOTOR_IA = "rf-hibrido-1.2"
_MAX_PREPARACIONES_IA = 64


@dataclass(frozen=True)
class ContextoIAPreparado:
    firma_preparacion: str
    mapa_actual_id: int
    puntos: list[PuntoRSSI]
    modelo_propagacion: ModeloPropagacion
    aps_existentes: list[dict]
    poligono_interes: list[dict]


_PREPARACIONES_IA: dict[tuple[int, int], ContextoIAPreparado] = {}


def _storage() -> LocalFilesystemStorage:
    return LocalFilesystemStorage(root=settings.storage_root)


def _payload_solicitud_ia(
    *,
    plano: Plano,
    conjunto: ConjuntoAP,
    body: RestriccionesIAIn,
    bssids_seleccionados: list[str],
) -> dict:
    return {
        "version_motor_ia": VERSION_MOTOR_IA,
        "plano_id": plano.id,
        "conjunto_fuente_id": conjunto.id,
        "banda_objetivo": conjunto.banda_objetivo,
        "bssids": sorted(bssids_seleccionados),
        "algoritmo": str(body.algoritmo),
        "resolucion": body.resolucion,
        "umbral_objetivo_dbm": body.umbral_objetivo_dbm,
        "cantidad_aps_propuestos": body.cantidad_aps_propuestos,
        "cantidad_recomendaciones": body.cantidad_recomendaciones,
    }


def _firma_solicitud_ia(payload: dict) -> str:
    serializado = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(serializado.encode(), usedforsecurity=False).hexdigest()


def _payload_preparacion_ia(
    *,
    plano: Plano,
    conjunto: ConjuntoAP,
    bssids_seleccionados: list[str],
    db: Session,
) -> dict:
    items = [
        {
            "bssid": item.bssid.lower(),
            "pos_x": item.pos_x,
            "pos_y": item.pos_y,
            "banda": item.banda,
            "radios": item.radios or [],
        }
        for item in sorted(conjunto.items, key=lambda item: item.bssid.lower())
    ]
    return {
        "version_motor_ia": VERSION_MOTOR_IA,
        "plano_id": plano.id,
        "conjunto_id": conjunto.id,
        "banda_objetivo": conjunto.banda_objetivo,
        "bssids": sorted(bssids_seleccionados),
        "items": items,
        "poligono_interes": plano.poligono_interes or [],
        "firma_mediciones": MedicionRepository(db).firma_mediciones_plano(
            plano_id=plano.id,
        ),
    }


def _firma_preparacion_ia(
    *,
    plano: Plano,
    conjunto: ConjuntoAP,
    bssids_seleccionados: list[str],
    db: Session,
) -> str:
    return _firma_solicitud_ia(
        _payload_preparacion_ia(
            plano=plano,
            conjunto=conjunto,
            bssids_seleccionados=bssids_seleccionados,
            db=db,
        )
    )


def _recordar_contexto_ia(
    *,
    plano_id: int,
    conjunto_id: int,
    contexto: ContextoIAPreparado,
) -> ContextoIAPreparado:
    if len(_PREPARACIONES_IA) >= _MAX_PREPARACIONES_IA:
        primera_clave = next(iter(_PREPARACIONES_IA))
        _PREPARACIONES_IA.pop(primera_clave, None)
    _PREPARACIONES_IA[(plano_id, conjunto_id)] = contexto
    return contexto


def _contexto_ia_preparado(
    *,
    plano: Plano,
    conjunto: ConjuntoAP,
    bssids_seleccionados: list[str],
    db: Session,
) -> ContextoIAPreparado | None:
    contexto = _PREPARACIONES_IA.get((plano.id, conjunto.id))
    if contexto is None:
        return None
    firma = _firma_preparacion_ia(
        plano=plano,
        conjunto=conjunto,
        bssids_seleccionados=bssids_seleccionados,
        db=db,
    )
    if contexto.firma_preparacion != firma:
        _PREPARACIONES_IA.pop((plano.id, conjunto.id), None)
        return None
    mapa_actual_existe = (
        db.query(MapaCalor.id)
        .filter(MapaCalor.id == contexto.mapa_actual_id)
        .first()
        is not None
    )
    if not mapa_actual_existe:
        _PREPARACIONES_IA.pop((plano.id, conjunto.id), None)
        return None
    return contexto


def _preparar_contexto_ia(
    *,
    plano: Plano,
    conjunto: ConjuntoAP,
    bssids_seleccionados: list[str],
    db: Session,
) -> ContextoIAPreparado:
    contexto = _contexto_ia_preparado(
        plano=plano,
        conjunto=conjunto,
        bssids_seleccionados=bssids_seleccionados,
        db=db,
    )
    if contexto is not None:
        return contexto

    mapa_actual, puntos = _mapa_actual(
        plano=plano,
        db=db,
        bssids_seleccionados=bssids_seleccionados,
        conjunto_ap_id=conjunto.id,
    )
    contexto = ContextoIAPreparado(
        firma_preparacion=_firma_preparacion_ia(
            plano=plano,
            conjunto=conjunto,
            bssids_seleccionados=bssids_seleccionados,
            db=db,
        ),
        mapa_actual_id=mapa_actual.id,
        puntos=puntos,
        modelo_propagacion=_modelo_calibrado_para_plano(
            plano=plano,
            db=db,
            conjunto=conjunto,
            bssids_seleccionados=bssids_seleccionados,
        ),
        aps_existentes=_aps_fuente_para_ia(conjunto=conjunto),
        poligono_interes=_requerir_poligono_interes(plano),
    )
    return _recordar_contexto_ia(
        plano_id=plano.id,
        conjunto_id=conjunto.id,
        contexto=contexto,
    )


def preparar_contexto_ia(
    *,
    plano_id: int,
    conjunto_id: int,
    db: Session,
) -> ContextoIAPreparado:
    plano = db.query(Plano).filter(Plano.id == plano_id).first()
    if plano is None:
        raise HTTPException(status_code=404, detail="Plano no encontrado.")
    if not plano.calibrado:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El plano seleccionado debe estar calibrado.",
        )
    conjunto = (
        db.query(ConjuntoAP)
        .filter(ConjuntoAP.id == conjunto_id, ConjuntoAP.plano_id == plano.id)
        .first()
    )
    if conjunto is None:
        raise HTTPException(status_code=404, detail="Conjunto AP no encontrado.")
    if conjunto.origen == "ia":
        raise HTTPException(
            status_code=422,
            detail="La preparación IA debe partir de un conjunto técnico.",
        )
    bssids_seleccionados = _requerir_bssids_medidos(
        plano=plano,
        conjunto=conjunto,
        db=db,
    )
    return _preparar_contexto_ia(
        plano=plano,
        conjunto=conjunto,
        bssids_seleccionados=bssids_seleccionados,
        db=db,
    )


def _clave_bloqueo_ia(*, plano_id: int, conjunto_id: int) -> int:
    firma = hashlib.sha1(
        f"ia:{plano_id}:{conjunto_id}".encode(),
        usedforsecurity=False,
    ).hexdigest()
    return int(firma[:15], 16)


def _bloquear_generacion_ia(
    *,
    db: Session,
    plano_id: int,
    conjunto_id: int,
) -> int | None:
    if db.get_bind().dialect.name != "postgresql":
        return None
    clave = _clave_bloqueo_ia(plano_id=plano_id, conjunto_id=conjunto_id)
    db.execute(text("SELECT pg_advisory_lock(:clave)"), {"clave": clave})
    return clave


def _liberar_generacion_ia(*, db: Session, clave: int | None) -> None:
    if clave is None:
        return
    db.execute(text("SELECT pg_advisory_unlock(:clave)"), {"clave": clave})


def _restricciones_coinciden_con_solicitud(
    *,
    restricciones: dict | None,
    payload: dict,
    firma: str,
) -> bool:
    if not isinstance(restricciones, dict):
        return False
    if restricciones.get("firma_solicitud") == firma:
        return True
    fuente = restricciones.get("fuente_entrada") or {}
    legado = {
        "version_motor_ia": restricciones.get("version_motor_ia", VERSION_MOTOR_IA),
        "plano_id": restricciones.get("plano_id"),
        "conjunto_fuente_id": fuente.get("conjunto_id"),
        "banda_objetivo": fuente.get("banda_objetivo"),
        "bssids": sorted(fuente.get("bssids") or []),
        "algoritmo": str(restricciones.get("algoritmo", "IDW")),
        "resolucion": restricciones.get("resolucion"),
        "umbral_objetivo_dbm": restricciones.get("umbral_objetivo_dbm"),
        "cantidad_aps_propuestos": restricciones.get("cantidad_aps_propuestos"),
        "cantidad_recomendaciones": restricciones.get("cantidad_recomendaciones"),
    }
    return legado == payload


def _conjuntos_ia_por_solicitud(
    *,
    db: Session,
    plano_id: int,
    conjunto_fuente_id: int,
    payload: dict,
    firma: str,
) -> list[ConjuntoAP]:
    candidatos = (
        db.query(ConjuntoAP)
        .filter(
            ConjuntoAP.plano_id == plano_id,
            ConjuntoAP.origen == "ia",
            ConjuntoAP.conjunto_origen_id == conjunto_fuente_id,
        )
        .order_by(ConjuntoAP.created_at.asc(), ConjuntoAP.id.asc())
        .all()
    )
    return [
        conjunto
        for conjunto in candidatos
        if _restricciones_coinciden_con_solicitud(
            restricciones=conjunto.restricciones_ia,
            payload=payload,
            firma=firma,
        )
    ]


def _eliminar_conjuntos_ia_duplicados(
    *,
    db: Session,
    conjuntos: list[ConjuntoAP],
    conservar: int,
) -> list[ConjuntoAP]:
    conservados = conjuntos[:conservar]
    duplicados = conjuntos[conservar:]
    if not duplicados:
        return conservados
    for conjunto in duplicados:
        (
            db.query(LecturaRSSI)
            .filter(LecturaRSSI.conjunto_ap_id == conjunto.id)
            .delete(synchronize_session=False)
        )
        (
            db.query(MapaCalor)
            .filter(MapaCalor.conjunto_ap_id == conjunto.id)
            .delete(synchronize_session=False)
        )
        db.delete(conjunto)
    db.commit()
    for conjunto in conservados:
        db.refresh(conjunto)
    return conservados


def _respuesta_ia_existente(
    *,
    db: Session,
    request: Request,
    conjunto_fuente: ConjuntoAP,
    mapa_actual: MapaCalor,
    payload: dict,
    firma: str,
) -> ConjuntosIAGeneradosOut | None:
    cantidad = int(payload["cantidad_recomendaciones"])
    conjuntos = _conjuntos_ia_por_solicitud(
        db=db,
        plano_id=int(payload["plano_id"]),
        conjunto_fuente_id=int(payload["conjunto_fuente_id"]),
        payload=payload,
        firma=firma,
    )
    if len(conjuntos) < cantidad:
        return None
    conjuntos = _eliminar_conjuntos_ia_duplicados(
        db=db,
        conjuntos=conjuntos,
        conservar=cantidad,
    )
    mapas = (
        db.query(MapaCalor)
        .filter(MapaCalor.conjunto_ap_id.in_([conjunto.id for conjunto in conjuntos]))
        .order_by(MapaCalor.created_at.asc(), MapaCalor.id.asc())
        .all()
    )
    return ConjuntosIAGeneradosOut(
        conjunto_base_id=conjunto_fuente.id,
        mapa_actual=_mapa_resumen_out(mapa_actual, request),
        conjuntos=[_conjunto_out(conjunto) for conjunto in conjuntos],
        mapas_proyectados=[_mapa_resumen_out(mapa, request) for mapa in mapas],
    )


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


def _proyecto_preparacion_ia(
    *,
    proyecto_id: int,
    current_user: Usuario,
    db: Session,
) -> Proyecto:
    repo = ProyectoRepository(db)
    if current_user.rol == "admin":
        proyecto = repo.obtener_por_id_admin(proyecto_id=proyecto_id)
    else:
        proyecto = repo.obtener_por_id(
            proyecto_id=proyecto_id,
            tecnico_id=current_user.id,
        )
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
    mapa_existente = next(
        (
            mapa
            for mapa in mapa_repo.listar_por_clave_conjunto(
                conjunto_ap_id=conjunto_ap_id,
                modo_generacion="CONJUNTO_COMPLETO",
                algoritmo="IDW",
                bssids=bssids_seleccionados,
            )
            if not mapa.ruta_imagen.startswith("heatmaps/ia_actual_")
        ),
        None,
    )
    if mapa_existente is not None:
        return mapa_existente, puntos

    poligono_interes = _requerir_poligono_interes(plano)
    firma = hashlib.sha1(
        (
            f"ia-actual-v2-no-deteccion:{plano.id}:conjunto:{conjunto_ap_id}:"
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
    conjunto = db.get(ConjuntoAP, conjunto_ap_id)
    if conjunto is None:
        raise HTTPException(status_code=404, detail="Conjunto AP no encontrado.")
    items_por_bssid = {item.bssid.lower(): item for item in conjunto.items}
    aps_por_bssid = {
        ap["bssid"]: ap for ap in MedicionRepository(db).listar_aps_por_plano(plano_id=plano.id)
    }
    aps_interes = []
    for bssid in bssids_seleccionados:
        item = items_por_bssid.get(bssid.lower())
        ap = aps_por_bssid.get(bssid.lower())
        if item is None or ap is None:
            continue
        if item.pos_x is None or item.pos_y is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "Debe ubicar todos los APs del conjunto sobre el plano antes "
                    "de preparar IA."
                ),
            )
        aps_interes.append(
            {
                "bssid": bssid.lower(),
                "ssid": item.ssid_snapshot or ap["ssid"],
                "canal": item.canal_snapshot,
                "frecuencia_mhz": ap.get("frecuencia_mhz"),
                "rssi_promedio": item.rssi_promedio_snapshot or ap["rssi_promedio"],
                "pos_x": item.pos_x,
                "pos_y": item.pos_y,
                "cantidad_puntos": ap["cantidad_puntos"],
            }
        )
    if not aps_interes:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El conjunto no tiene APs válidos para preparar IA.",
        )
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
    conjunto: ConjuntoAP,
    bssids_seleccionados: list[str],
) -> ModeloPropagacion:
    items_por_bssid = {item.bssid.lower(): item for item in conjunto.items}
    query = (
        db.query(LecturaRSSI, PuntoMedicion)
        .join(PuntoMedicion, LecturaRSSI.punto_id == PuntoMedicion.id)
        .filter(PuntoMedicion.plano_id == plano.id)
        .filter(LecturaRSSI.origen == ORIGEN_CAMPO)
        .filter(LecturaRSSI.bssid.in_(bssids_seleccionados))
    )
    muestras: list[MuestraCalibracionRF] = []
    muestras_espaciales: list[dict] = []
    metros_por_pixel = plano.escala_m_por_px or 1.0
    for lectura, punto in query.all():
        item = items_por_bssid.get(lectura.bssid.lower())
        if item is None or item.pos_x is None or item.pos_y is None:
            continue
        if lectura.rssi <= -120 or lectura.rssi >= 0:
            continue
        distancia_px = math.hypot(punto.pos_x - item.pos_x, punto.pos_y - item.pos_y)
        banda = item.banda or _banda_lectura(lectura)
        radio_tx = _radio_tx_principal(item.radios)
        muestras.append(
            # Solo se usa TX Power cuando fue declarado con fuente y confianza
            # suficientes; RSSI sigue siendo la evidencia central del survey.
            MuestraCalibracionRF(
                distancia_m=max(1.0, distancia_px * metros_por_pixel),
                banda=banda,
                rssi_dbm=float(lectura.rssi),
                potencia_dbm=radio_tx.get("potencia_dbm"),
                ganancia_dbi=radio_tx.get("ganancia_dbi", 2.14),
                perdida_cable_db=radio_tx.get("perdida_cable_db", 0.0),
            )
        )
        muestras_espaciales.append(
            {
                "x_px": float(punto.pos_x),
                "y_px": float(punto.pos_y),
                "distancia_px": distancia_px,
                "banda": banda,
                "rssi_dbm": float(lectura.rssi),
            }
        )
    modelo = ModeloPropagacion.calibrar_desde_muestras(muestras)
    correcciones = [
        CorreccionEspacialRF(
            x_px=muestra["x_px"],
            y_px=muestra["y_px"],
            banda=muestra["banda"],
            error_db=muestra["rssi_dbm"]
            - modelo.predecir_rssi(
                distancia_px=muestra["distancia_px"],
                metros_por_pixel=metros_por_pixel,
                banda=muestra["banda"],
                aplicar_correccion_espacial=False,
            ),
        )
        for muestra in muestras_espaciales
    ]
    return modelo.con_correccion_espacial(correcciones)


def _banda_lectura(lectura: LecturaRSSI) -> str:
    if lectura.frecuencia_mhz is not None:
        return "2.4" if lectura.frecuencia_mhz < 3000 else "5"
    return "2.4" if lectura.canal is not None and lectura.canal <= 14 else "5"


def _aps_fuente_para_ia(*, conjunto: ConjuntoAP) -> list[dict]:
    return [
        {
            "id": item.id,
            "coord_x": item.pos_x,
            "coord_y": item.pos_y,
            "altura_m": item.altura_m or 2.5,
            "tipo_montaje": item.tipo_montaje or "TECHO",
            "restriccion_movimiento": "MOVIBLE",
            "verificado": item.pos_x is not None and item.pos_y is not None,
        }
        for item in conjunto.items
        if item.pos_x is not None and item.pos_y is not None
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


def _combinaciones_items(items: list[dict]) -> list[list[dict]]:
    combinaciones_items: list[list[dict]] = []
    for tamano in range(1, len(items) + 1):
        combinaciones_items.extend(list(combinations(items, tamano)))
    return [list(item) for item in combinaciones_items]


def _matriz_proyectada_desde_items(
    *,
    items: list[dict],
    modelo: ModeloPropagacion,
    ancho_px: int,
    alto_px: int,
    metros_por_pixel: float,
    banda: str,
    resolucion: int,
) -> list[list[float]]:
    coordenadas = [
        (float(item["pos_x"]), float(item["pos_y"]))
        for item in items
        if item.get("pos_x") is not None and item.get("pos_y") is not None
    ]
    matriz: list[list[float]] = []
    for fila in range(resolucion):
        y = ((fila + 0.5) / resolucion) * alto_px
        valores_fila: list[float] = []
        for col in range(resolucion):
            x = ((col + 0.5) / resolucion) * ancho_px
            mejor = max(
                modelo.predecir_rssi(
                    distancia_px=math.hypot(x - ap_x, y - ap_y),
                    metros_por_pixel=metros_por_pixel,
                    banda=banda,
                    punto_x=x,
                    punto_y=y,
                )
                for ap_x, ap_y in coordenadas
            )
            valores_fila.append(mejor)
        matriz.append(valores_fila)
    return matriz


def _lecturas_estimadas_desde_items(
    *,
    puntos: list[PuntoRSSI],
    items: list[dict],
    modelo: ModeloPropagacion,
    metros_por_pixel: float,
    banda: str,
) -> list[dict]:
    lecturas: list[dict] = []
    for item in items:
        radio_principal = _radio_principal(item.get("radios"))
        for punto in puntos:
            rssi = modelo.predecir_rssi(
                distancia_px=math.hypot(
                    punto.x - float(item["pos_x"]),
                    punto.y - float(item["pos_y"]),
                ),
                metros_por_pixel=metros_por_pixel,
                banda=banda,
                punto_x=punto.x,
                punto_y=punto.y,
                potencia_dbm=radio_principal.get("potencia_dbm"),
                ganancia_dbi=radio_principal.get("ganancia_dbi", 2.14),
                perdida_cable_db=radio_principal.get("perdida_cable_db", 0.0),
            )
            lecturas.append(
                {
                    "punto_id": punto.punto_id,
                    "ssid": item["ssid_snapshot"],
                    "bssid": item["bssid"],
                    "rssi": rssi,
                    "canal": item.get("canal_snapshot"),
                    "frecuencia_mhz": 2412 if banda == "2.4" else 5180,
                    "modelo_origen": VERSION_MOTOR_IA,
                    "incertidumbre_db": 6.0,
                }
            )
    return lecturas


def _modo_mapa_ia(*, cantidad_items: int, total_items: int) -> str:
    if cantidad_items == 1:
        return "INDIVIDUAL"
    if cantidad_items == total_items:
        return "PROYECTADO"
    return "SUBCONJUNTO"


@router_proyectos_escenarios.post(
    "/{proyecto_id}/conjuntos-ap/{conjunto_id}/preparacion-ia",
    response_model=PreparacionIAOut,
    status_code=status.HTTP_202_ACCEPTED,
)
def preparar_conjunto_ia(
    proyecto_id: int,
    conjunto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> PreparacionIAOut:
    proyecto = _proyecto_preparacion_ia(
        proyecto_id=proyecto_id,
        current_user=current_user,
        db=db,
    )
    conjunto = (
        db.query(ConjuntoAP)
        .join(Plano, ConjuntoAP.plano_id == Plano.id)
        .filter(ConjuntoAP.id == conjunto_id, Plano.proyecto_id == proyecto.id)
        .first()
    )
    if conjunto is None:
        raise HTTPException(status_code=404, detail="Conjunto AP no encontrado.")
    contexto = preparar_contexto_ia(
        plano_id=conjunto.plano_id,
        conjunto_id=conjunto.id,
        db=db,
    )
    return PreparacionIAOut(
        plano_id=conjunto.plano_id,
        conjunto_id=conjunto.id,
        mapa_actual_id=contexto.mapa_actual_id,
        cantidad_puntos=len(contexto.puntos),
    )


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
    payload_solicitud = _payload_solicitud_ia(
        plano=plano,
        conjunto=conjunto_fuente,
        body=body,
        bssids_seleccionados=bssids_seleccionados,
    )
    firma_solicitud = _firma_solicitud_ia(payload_solicitud)
    clave_bloqueo = _bloquear_generacion_ia(
        db=db,
        plano_id=plano.id,
        conjunto_id=conjunto_fuente.id,
    )
    try:
        return _generar_conjuntos_ia_bloqueado(
            proyecto=proyecto,
            plano=plano,
            conjunto_fuente=conjunto_fuente,
            bssids_seleccionados=bssids_seleccionados,
            payload_solicitud=payload_solicitud,
            firma_solicitud=firma_solicitud,
            body=body,
            request=request,
            db=db,
            current_user=current_user,
        )
    finally:
        _liberar_generacion_ia(db=db, clave=clave_bloqueo)


def _generar_conjuntos_ia_bloqueado(
    *,
    proyecto: Proyecto,
    plano: Plano,
    conjunto_fuente: ConjuntoAP,
    bssids_seleccionados: list[str],
    payload_solicitud: dict,
    firma_solicitud: str,
    body: RestriccionesIAIn,
    request: Request,
    db: Session,
    current_user: Usuario,
) -> ConjuntosIAGeneradosOut:
    contexto_preparado = _contexto_ia_preparado(
        plano=plano,
        conjunto=conjunto_fuente,
        bssids_seleccionados=bssids_seleccionados,
        db=db,
    )
    if contexto_preparado is not None:
        mapa_actual = db.get(MapaCalor, contexto_preparado.mapa_actual_id)
        puntos = contexto_preparado.puntos
    else:
        mapa_actual, puntos = _mapa_actual(
            plano=plano,
            db=db,
            bssids_seleccionados=bssids_seleccionados,
            conjunto_ap_id=conjunto_fuente.id,
        )
    if mapa_actual is None:
        mapa_actual, puntos = _mapa_actual(
            plano=plano,
            db=db,
            bssids_seleccionados=bssids_seleccionados,
            conjunto_ap_id=conjunto_fuente.id,
        )
    respuesta_existente = _respuesta_ia_existente(
        db=db,
        request=request,
        conjunto_fuente=conjunto_fuente,
        mapa_actual=mapa_actual,
        payload=payload_solicitud,
        firma=firma_solicitud,
    )
    if respuesta_existente is not None:
        return respuesta_existente

    if contexto_preparado is None:
        contexto_preparado = _preparar_contexto_ia(
            plano=plano,
            conjunto=conjunto_fuente,
            bssids_seleccionados=bssids_seleccionados,
            db=db,
        )
    modelo_propagacion = contexto_preparado.modelo_propagacion
    aps_existentes = contexto_preparado.aps_existentes
    limite_aps = body.cantidad_aps_propuestos
    banda_objetivo = conjunto_fuente.banda_objetivo
    poligono_interes = contexto_preparado.poligono_interes
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
        bandas=[banda_objetivo],
        aps_existentes=aps_existentes,
        cantidad_recomendaciones=body.cantidad_recomendaciones,
        poligono_interes=poligono_interes,
    )
    conjunto_repo = ConjuntoAPRepository(db)
    mapa_repo = MapaCalorRepository(db)
    med_repo = MedicionRepository(db)
    conjuntos_ia: list[ConjuntoAP] = []
    mapas_proyectados: list[MapaCalor] = []
    puntos_por_mapa_id: dict[int, list[PuntoRSSI]] = {}
    restricciones = body.model_dump(exclude_none=True)
    restricciones["fuente_entrada"]["nombre"] = conjunto_fuente.nombre
    restricciones["fuente_entrada"]["proposito"] = conjunto_fuente.proposito
    restricciones["fuente_entrada"]["banda_objetivo"] = conjunto_fuente.banda_objetivo
    restricciones["fuente_entrada"]["bssids"] = bssids_seleccionados
    restricciones["cantidad_aps_propuestos"] = limite_aps
    restricciones["firma_solicitud"] = firma_solicitud
    restricciones["version_motor_ia"] = VERSION_MOTOR_IA
    mascara_mapa = mascara_poligono(
        poligono=poligono_interes,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        resolucion=body.resolucion,
    )
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
            banda_objetivo=conjunto_fuente.banda_objetivo,
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
                "banda_objetivo": alternativa.banda,
                "cantidad_aps_solicitada": limite_aps,
                "lecturas_simuladas": alternativa.valores_proyectados,
                "cantidad_lecturas_simuladas": len(alternativa.valores_proyectados),
            },
            restricciones_ia=restricciones,
            version_motor_ia=VERSION_MOTOR_IA,
        )
        conjuntos_ia.append(conjunto_ia)
        lecturas_estimadas = _lecturas_estimadas_desde_items(
            puntos=puntos,
            items=items,
            modelo=modelo_propagacion,
            metros_por_pixel=plano.escala_m_por_px or 1.0,
            banda=alternativa.banda,
        )
        med_repo.reemplazar_lecturas_estimadas(
            conjunto_ap_id=conjunto_ia.id,
            lecturas=lecturas_estimadas,
        )
        conjunto_ia.metricas_ia = {
            **(conjunto_ia.metricas_ia or {}),
            "lecturas_estimadas": lecturas_estimadas,
            "cantidad_lecturas_estimadas": len(lecturas_estimadas),
            "lecturas_simuladas": lecturas_estimadas,
            "cantidad_lecturas_simuladas": len(lecturas_estimadas),
        }
        db.commit()
        db.refresh(conjunto_ia)
        for combo_idx, items_combo in enumerate([items], start=1):
            bssids_combo = [item["bssid"] for item in items_combo]
            puntos_combo = med_repo.listar_puntos_rssi_heatmap(
                plano_id=plano.id,
                bssids=bssids_combo,
                origen=ORIGEN_IA_ESTIMADA,
                conjunto_ap_id=conjunto_ia.id,
            )
            matriz_combo = InterpolacionService().interpolar(
                puntos=puntos_combo,
                ancho_px=plano.ancho_px,
                alto_px=plano.alto_px,
                resolucion=body.resolucion,
                algoritmo=body.algoritmo,
            )
            ruta = (
                f"heatmaps/ia_proyectado_{proyecto.id}_{idx}_{combo_idx}_"
                f"{secrets.token_hex(8)}.png"
            )
            _storage().save(
                HeatmapImageService().render_png(
                    matriz_combo,
                    mascara=mascara_mapa,
                ),
                ruta,
            )
            firma = hashlib.sha1(
                (
                    f"ia-proyectado-lectura-rssi:{proyecto.id}:{conjunto_ia.id}:"
                    f"{combo_idx}:{body.algoritmo}:{secrets.token_hex(8)}"
                ).encode(),
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
                for item in items_combo
            ]
            mapa_proyectado = mapa_repo.crear(
                plano_id=plano.id,
                conjunto_ap_id=conjunto_ia.id,
                modo_generacion=_modo_mapa_ia(
                    cantidad_items=len(items_combo),
                    total_items=len(items),
                ),
                algoritmo=body.algoritmo,
                resolucion=body.resolucion,
                bssid=items_combo[0]["bssid"],
                ssid=conjunto_ia.nombre,
                ap_pos_x=items_combo[0]["pos_x"],
                ap_pos_y=items_combo[0]["pos_y"],
                aps_interes=aps_interes,
                bssids_generacion=bssids_combo,
                matriz=matriz_combo,
                escala=ESCALA_CWNA,
                ruta_imagen=ruta,
                cantidad_puntos=len(puntos_combo),
                rssi_min=min(punto.rssi for punto in puntos_combo),
                rssi_max=max(punto.rssi for punto in puntos_combo),
                firma_mediciones=firma,
            )
            mapas_proyectados.append(mapa_proyectado)
            puntos_por_mapa_id[mapa_proyectado.id] = puntos_combo

    return ConjuntosIAGeneradosOut(
        conjunto_base_id=conjunto_fuente.id,
        mapa_actual=_mapa_resumen_out(mapa_actual, request),
        conjuntos=[_conjunto_out(conjunto) for conjunto in conjuntos_ia],
        mapas_proyectados=[
            _mapa_resumen_out(mapa, request, puntos=puntos_por_mapa_id.get(mapa.id))
            for mapa in mapas_proyectados
        ],
    )
