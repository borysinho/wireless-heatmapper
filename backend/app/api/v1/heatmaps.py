"""Endpoints de heatmap y conjuntos de AP.

Sprint 4 — PB-05 (Generar mapa de calor).
"""

import hashlib
import json
import math
import secrets
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.ai.modelo_propagacion import ModeloPropagacion
from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.heatmap import MapaCalor
from app.models.share import TokenEnlaceCliente
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
from app.repositories.plano_repository import PlanoRepository
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.heatmap import (
    ActualizarUbicacionAPConjuntoIn,
    APDisponibleOut,
    ConfiguracionRadioAPIn,
    ConjuntoAPActualizarIn,
    ConjuntoAPCrearIn,
    ConjuntoAPItemOut,
    ConjuntoAPOut,
    GenerarHeatmapConjuntoIn,
    GenerarHeatmapsFaltantesIn,
    MapaCalorOut,
    MapaCalorResumenOut,
    PuntoLecturaHeatmapOut,
)
from app.services.geometria_service import mascara_poligono
from app.services.interpolacion_service import (
    ESCALA_CWNA,
    HeatmapImageService,
    InterpolacionService,
    PuntoRSSI,
)
from app.storage import LocalFilesystemStorage, generar_url_firmada, verificar_firma

router_planos_heatmap = APIRouter(prefix="/planos", tags=["heatmaps"])
router_mapas = APIRouter(prefix="/mapas", tags=["heatmaps"])
router_conjuntos_ap = APIRouter(prefix="/conjuntos-ap", tags=["heatmaps"])


def _storage() -> LocalFilesystemStorage:
    return LocalFilesystemStorage(root=settings.storage_root)


def _firmar(ruta: str, request: Request) -> str:
    url = generar_url_firmada(
        ruta_relativa=ruta,
        secret=settings.storage_url_secret,
        base_url=settings.public_api_url,
        ttl_seconds=settings.storage_url_ttl_seconds,
    )
    return url.replace("/planos/archivo/", "/mapas/archivo/", 1)


def _verificar_ownership_plano(
    *,
    plano_id: int,
    current_user: Usuario,
    db: Session,
):
    plano = PlanoRepository(db).obtener_por_id(plano_id=plano_id)
    if plano is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano no encontrado.",
        )
    proyecto_repo = ProyectoRepository(db)
    proyecto = (
        proyecto_repo.obtener_por_id_admin(proyecto_id=plano.proyecto_id)
        if current_user.rol == "admin"
        else proyecto_repo.obtener_por_id(
            proyecto_id=plano.proyecto_id,
            tecnico_id=current_user.id,
        )
    )
    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano no encontrado.",
        )
    return plano


def _verificar_ownership_mapa(
    *,
    mapa_id: int,
    current_user: Usuario,
    db: Session,
) -> MapaCalor:
    mapa = MapaCalorRepository(db).obtener_por_id(mapa_id=mapa_id)
    if mapa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mapa de calor no encontrado.",
        )
    _verificar_ownership_plano(
        plano_id=mapa.plano_id,
        current_user=current_user,
        db=db,
    )
    return mapa


def _mapa_out(
    mapa: MapaCalor,
    request: Request,
    *,
    puntos: list[PuntoRSSI] | None = None,
    resumen_puntos: dict[int, dict] | None = None,
) -> MapaCalorOut:
    aps_interes = mapa.aps_interes or [
        {
            "bssid": mapa.bssid,
            "ssid": mapa.ssid,
            "canal": None,
            "frecuencia_mhz": None,
            "rssi_promedio": 0,
            "pos_x": mapa.ap_pos_x,
            "pos_y": mapa.ap_pos_y,
            "cantidad_puntos": mapa.cantidad_puntos,
        }
    ]
    puntos_lectura = puntos or _puntos_simulados_desde_metricas(mapa)
    rssi_promedio = (
        sum(punto.rssi for punto in puntos_lectura) / len(puntos_lectura)
        if puntos_lectura
        else (mapa.rssi_min + mapa.rssi_max) / 2
    )
    return MapaCalorOut(
        id=mapa.id,
        plano_id=mapa.plano_id,
        conjunto_ap_id=mapa.conjunto_ap_id,
        modo_generacion=mapa.modo_generacion,
        algoritmo=mapa.algoritmo,
        resolucion=mapa.resolucion,
        bssid=mapa.bssid,
        ssid=mapa.ssid,
        ap_pos_x=mapa.ap_pos_x,
        ap_pos_y=mapa.ap_pos_y,
        aps_interes=aps_interes,
        bssids_generacion=mapa.bssids_generacion or [ap["bssid"] for ap in aps_interes],
        url_imagen=_firmar(mapa.ruta_imagen, request),
        matriz=mapa.matriz,
        escala=mapa.escala,
        cantidad_puntos=mapa.cantidad_puntos,
        rssi_min=mapa.rssi_min,
        rssi_max=mapa.rssi_max,
        rssi_promedio=round(rssi_promedio, 2),
        puntos_lectura=[
            PuntoLecturaHeatmapOut(
                punto_id=punto.punto_id,
                pos_x=punto.x,
                pos_y=punto.y,
                rssi=punto.rssi,
                total_lecturas=(resumen_puntos or {})
                .get(punto.punto_id, {})
                .get("total_lecturas", 0),
                detalle_aps=(resumen_puntos or {})
                .get(punto.punto_id, {})
                .get("detalle_aps", []),
            )
            for punto in puntos_lectura
        ],
        poligono_interes=[
            {"x": float(punto["x"]), "y": float(punto["y"])}
            for punto in (mapa.plano.poligono_interes or [])
        ],
        advertencias=_advertencias_heatmap(
            cantidad_puntos=len(puntos_lectura) or mapa.cantidad_puntos,
            aps_interes=aps_interes,
        ),
        created_at=mapa.created_at,
    )


def _mapa_resumen_out(
    mapa: MapaCalor,
    request: Request,
    *,
    puntos: list[PuntoRSSI] | None = None,
) -> MapaCalorResumenOut:
    aps_interes = mapa.aps_interes or [
        {
            "bssid": mapa.bssid,
            "ssid": mapa.ssid,
            "canal": None,
            "frecuencia_mhz": None,
            "rssi_promedio": 0,
            "pos_x": mapa.ap_pos_x,
            "pos_y": mapa.ap_pos_y,
            "cantidad_puntos": mapa.cantidad_puntos,
        }
    ]
    puntos_lectura = puntos or _puntos_simulados_desde_metricas(mapa)
    rssi_promedio = (
        sum(punto.rssi for punto in puntos_lectura) / len(puntos_lectura)
        if puntos_lectura
        else (mapa.rssi_min + mapa.rssi_max) / 2
    )
    return MapaCalorResumenOut(
        id=mapa.id,
        plano_id=mapa.plano_id,
        conjunto_ap_id=mapa.conjunto_ap_id,
        modo_generacion=mapa.modo_generacion,
        algoritmo=mapa.algoritmo,
        resolucion=mapa.resolucion,
        bssid=mapa.bssid,
        ssid=mapa.ssid,
        aps_interes=aps_interes,
        bssids_generacion=mapa.bssids_generacion or [ap["bssid"] for ap in aps_interes],
        url_imagen=_firmar(mapa.ruta_imagen, request),
        cantidad_puntos=mapa.cantidad_puntos,
        rssi_min=mapa.rssi_min,
        rssi_max=mapa.rssi_max,
        rssi_promedio=round(rssi_promedio, 2),
        created_at=mapa.created_at,
    )


def _mapa_resumen_desde_out(mapa: MapaCalorOut) -> MapaCalorResumenOut:
    return MapaCalorResumenOut(
        id=mapa.id,
        plano_id=mapa.plano_id,
        conjunto_ap_id=mapa.conjunto_ap_id,
        modo_generacion=mapa.modo_generacion,
        algoritmo=mapa.algoritmo,
        resolucion=mapa.resolucion,
        bssid=mapa.bssid,
        ssid=mapa.ssid,
        aps_interes=mapa.aps_interes,
        bssids_generacion=mapa.bssids_generacion,
        url_imagen=mapa.url_imagen,
        cantidad_puntos=mapa.cantidad_puntos,
        rssi_min=mapa.rssi_min,
        rssi_max=mapa.rssi_max,
        rssi_promedio=mapa.rssi_promedio,
        created_at=mapa.created_at,
    )


def _puntos_simulados_desde_metricas(mapa: MapaCalor) -> list[PuntoRSSI]:
    if mapa.modo_generacion != "PROYECTADO" or mapa.conjunto_ap is None:
        return []
    metricas = mapa.conjunto_ap.metricas_ia or {}
    lecturas = metricas.get("lecturas_simuladas") or []
    if not isinstance(lecturas, list):
        return []
    banda_objetivo = metricas.get("banda_objetivo")
    puntos_por_id: dict[int, PuntoRSSI] = {}
    for lectura in lecturas:
        if not isinstance(lectura, dict):
            continue
        if banda_objetivo and lectura.get("banda") != banda_objetivo:
            continue
        punto_id = lectura.get("punto_id") or lectura.get("punto_medicion_id")
        pos_x = lectura.get("pos_x")
        pos_y = lectura.get("pos_y")
        rssi = lectura.get("rssi") or lectura.get("rssi_proyectado_dbm")
        if punto_id is None or pos_x is None or pos_y is None or rssi is None:
            continue
        puntos_por_id[int(punto_id)] = PuntoRSSI(
            punto_id=int(punto_id),
            x=float(pos_x),
            y=float(pos_y),
            rssi=float(rssi),
        )
    return list(puntos_por_id.values())


def _advertencias_heatmap(
    *,
    cantidad_puntos: int,
    aps_interes: list[dict],
) -> list[str]:
    advertencias: list[str] = []
    if cantidad_puntos < 10:
        advertencias.append(
            "Baja densidad de muestras: el heatmap puede verse uniforme. "
            "Agrega más puntos de lectura distribuidos sobre el plano."
        )
    aps_con_pocas_muestras = [
        ap["ssid"] or ap["bssid"]
        for ap in aps_interes
        if int(ap.get("cantidad_puntos") or 0) < 5
    ]
    if aps_con_pocas_muestras:
        advertencias.append(
            "Uno o más APs seleccionados tienen pocas lecturas: "
            + ", ".join(aps_con_pocas_muestras)
            + "."
        )
    return advertencias


def _normalizar_bssids(bssids: list[str]) -> list[str]:
    normalizados: list[str] = []
    for bssid in bssids:
        valor = bssid.strip().lower()
        if valor and valor not in normalizados:
            normalizados.append(valor)
    return normalizados


def _resolver_aps_interes(
    *,
    aps: list[dict],
    bssids: list[str],
    ap_pos_x: list[float] | None,
    ap_pos_y: list[float] | None,
) -> list[dict]:
    if (ap_pos_x is None) != (ap_pos_y is None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Las coordenadas X/Y de los APs de interés deben enviarse juntas.",
        )
    if ap_pos_x is not None and len(ap_pos_x) != len(bssids):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "La cantidad de coordenadas X no coincide con los APs seleccionados."
            ),
        )
    if ap_pos_y is not None and len(ap_pos_y) != len(bssids):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "La cantidad de coordenadas Y no coincide con los APs seleccionados."
            ),
        )
    if ap_pos_x is not None and any(pos < 0 for pos in ap_pos_x):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Las coordenadas X de los APs de interés no pueden ser negativas.",
        )
    if ap_pos_y is not None and any(pos < 0 for pos in ap_pos_y):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Las coordenadas Y de los APs de interés no pueden ser negativas.",
        )

    por_bssid = {ap["bssid"]: ap for ap in aps}
    faltantes = [bssid for bssid in bssids if bssid not in por_bssid]
    if faltantes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Uno o más APs seleccionados no existen en las mediciones del plano."
            ),
        )

    seleccionados: list[dict] = []
    for idx, bssid in enumerate(bssids):
        ap = por_bssid[bssid]
        seleccionados.append(
            {
                "bssid": bssid,
                "ssid": ap["ssid"],
                "canal": ap["canal"],
                "frecuencia_mhz": ap["frecuencia_mhz"],
                "rssi_promedio": ap["rssi_promedio"],
                "pos_x": ap_pos_x[idx] if ap_pos_x is not None else ap["pos_x"],
                "pos_y": ap_pos_y[idx] if ap_pos_y is not None else ap["pos_y"],
                "cantidad_puntos": ap["cantidad_puntos"],
            }
        )
    return seleccionados


def _normalizar_configuraciones_radio(
    configuraciones: list[ConfiguracionRadioAPIn] | None,
) -> dict[str, ConfiguracionRadioAPIn]:
    return {
        config.bssid.strip().lower(): config
        for config in configuraciones or []
    }


def _radio_desde_configuracion(
    *,
    config: ConfiguracionRadioAPIn | None,
    banda: str | None,
) -> list[dict] | None:
    if config is None or config.potencia_tx_dbm is None:
        return None
    radio = {
        "banda": banda,
        "potencia_dbm": float(config.potencia_tx_dbm),
        "fuente_potencia": config.fuente_potencia,
        "confianza_potencia": config.confianza_potencia,
    }
    if config.ganancia_dbi is not None:
        radio["ganancia_dbi"] = float(config.ganancia_dbi)
    if config.perdida_cable_db is not None:
        radio["perdida_cable_db"] = float(config.perdida_cable_db)
    return [radio]


def _radio_tx_principal(radios) -> dict:
    radio = _radio_principal(radios)
    if not radio:
        return {}
    potencia = radio.get("potencia_dbm")
    if potencia is None:
        potencia = radio.get("potencia_tx_dbm")
    if potencia is None:
        return {}
    fuente = str(radio.get("fuente_potencia") or "desconocida").lower()
    confianza = str(radio.get("confianza_potencia") or "baja").lower()
    radio_normalizada = {
        **radio,
        "potencia_dbm": float(potencia),
        "fuente_potencia": fuente,
        "confianza_potencia": confianza,
    }
    if fuente not in {"manual", "controlador"}:
        return {}
    if confianza not in {"media", "alta"}:
        return {}
    return radio_normalizada


def _metadata_potencia_tx(radios) -> dict:
    radio = _radio_principal(radios)
    if not radio:
        return {
            "potencia_tx_dbm": None,
            "fuente_potencia": None,
            "confianza_potencia": None,
        }
    potencia = radio.get("potencia_dbm")
    if potencia is None:
        potencia = radio.get("potencia_tx_dbm")
    return {
        "potencia_tx_dbm": float(potencia) if potencia is not None else None,
        "fuente_potencia": radio.get("fuente_potencia"),
        "confianza_potencia": radio.get("confianza_potencia"),
    }


def _resolver_items_conjunto(
    *,
    aps: list[dict],
    bssids: list[str],
    configuraciones_radio: list[ConfiguracionRadioAPIn] | None = None,
    items_existentes: list | None = None,
) -> list[dict]:
    bssids_norm = _normalizar_bssids(bssids)
    if not bssids_norm:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe seleccionar al menos un AP para el conjunto.",
        )
    por_bssid = {ap["bssid"]: ap for ap in aps}
    faltantes = [bssid for bssid in bssids_norm if bssid not in por_bssid]
    if faltantes:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Uno o más APs no existen en las mediciones del plano.",
        )
    config_por_bssid = _normalizar_configuraciones_radio(configuraciones_radio)
    radios_existentes = {
        item.bssid.lower(): item.radios
        for item in items_existentes or []
        if getattr(item, "radios", None)
    }
    return [
        {
            "bssid": bssid,
            "ssid_snapshot": por_bssid[bssid]["ssid"],
            "canal_snapshot": por_bssid[bssid]["canal"],
            "rssi_promedio_snapshot": por_bssid[bssid]["rssi_promedio"],
            "pos_x": por_bssid[bssid]["pos_x"],
            "pos_y": por_bssid[bssid]["pos_y"],
            "banda": _banda_ap(por_bssid[bssid]),
            "radios": _radio_desde_configuracion(
                config=config_por_bssid.get(bssid),
                banda=_banda_ap(por_bssid[bssid]),
            )
            or radios_existentes.get(bssid),
        }
        for bssid in bssids_norm
    ]


def _banda_ap(ap: dict) -> str | None:
    frecuencia = ap.get("frecuencia_mhz")
    if frecuencia is None:
        return None
    return "2.4" if int(frecuencia) < 3000 else "5"


def _validar_banda_items(*, items: list[dict], banda_objetivo: str) -> None:
    fuera_de_banda = [
        item["bssid"]
        for item in items
        if item.get("banda") is not None and item["banda"] != banda_objetivo
    ]
    if fuera_de_banda:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "El conjunto contiene APs que no pertenecen a la banda "
                f"{banda_objetivo} GHz."
            ),
        )


def _clave_bssids(bssids: list[str]) -> tuple[str, ...]:
    return tuple(sorted(bssid.lower() for bssid in bssids))


def _mapas_objetivo_conjunto(
    *,
    bssids: list[str],
    origen_conjunto: str,
) -> list[tuple[list[str], str]]:
    modo_global = "PROYECTADO" if origen_conjunto == "ia" else "CONJUNTO_COMPLETO"
    if len(bssids) == 1:
        return [(bssids, modo_global)]
    return [(bssids, modo_global)] + [([bssid], "INDIVIDUAL") for bssid in bssids]


def _clave_publicacion_mapa(mapa: MapaCalor) -> tuple[str, tuple[str, ...]]:
    bssids = mapa.bssids_generacion or [mapa.bssid]
    return (mapa.algoritmo.upper(), _clave_bssids(bssids))


def _actualizar_enlaces_cliente_por_reemplazo_mapas(
    *,
    db: Session,
    proyecto_id: int,
    reemplazos_mapa_id: dict[int, int],
    conjunto_id: int | None = None,
    nuevos_mapa_ids: list[int] | None = None,
) -> None:
    nuevos_mapa_ids = nuevos_mapa_ids or []
    if not reemplazos_mapa_id and not nuevos_mapa_ids:
        return

    enlaces = (
        db.query(TokenEnlaceCliente)
        .filter(TokenEnlaceCliente.proyecto_id == proyecto_id)
        .all()
    )
    hubo_cambios = False
    for enlace in enlaces:
        contenido = dict(enlace.contenido or {})
        mapa_ids = contenido.get("mapa_ids") or []
        conjunto_ids = contenido.get("conjunto_ids") or []
        if not isinstance(mapa_ids, list):
            continue
        if not isinstance(conjunto_ids, list):
            conjunto_ids = []

        actualizados: list[int] = []
        cambio_en_enlace = False
        for mapa_id in mapa_ids:
            try:
                mapa_id_int = int(mapa_id)
            except (TypeError, ValueError):
                continue

            nuevo_mapa_id = reemplazos_mapa_id.get(mapa_id_int)
            if nuevo_mapa_id is not None:
                actualizados.append(nuevo_mapa_id)
                cambio_en_enlace = True
            else:
                actualizados.append(mapa_id_int)

        conjunto_ids_norm = [
            item_int
            for item in conjunto_ids
            if (item_int := _entero_o_none(item)) is not None
        ]
        comparte_conjunto = conjunto_id is not None and conjunto_id in conjunto_ids_norm
        if comparte_conjunto:
            for mapa_id in nuevos_mapa_ids:
                if mapa_id not in actualizados:
                    actualizados.append(mapa_id)
                    cambio_en_enlace = True

        if not cambio_en_enlace:
            continue

        contenido["mapa_ids"] = list(dict.fromkeys(actualizados))
        enlace.contenido = contenido
        flag_modified(enlace, "contenido")
        hubo_cambios = True

    if hubo_cambios:
        db.commit()


def _entero_o_none(valor: object) -> int | None:
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _algoritmos_faltantes(body: GenerarHeatmapsFaltantesIn) -> list[str]:
    solicitados = body.algoritmos
    if solicitados is None:
        solicitados = [body.algoritmo] if body.algoritmo is not None else ["IDW"]
    return list(dict.fromkeys(algoritmo.upper() for algoritmo in solicitados))


def _lecturas_metricas_ia(conjunto, bssids_requeridos: set[str]) -> list[dict]:
    metricas = conjunto.metricas_ia or {}
    lecturas_base = (
        metricas.get("lecturas_estimadas") or metricas.get("lecturas_simuladas") or []
    )
    if not isinstance(lecturas_base, list):
        return []

    lecturas: list[dict] = []
    bssids_presentes: set[str] = set()
    for lectura in lecturas_base:
        if not isinstance(lectura, dict):
            continue
        bssid = str(lectura.get("bssid") or "").lower()
        punto_id = lectura.get("punto_id") or lectura.get("punto_medicion_id")
        rssi = lectura.get("rssi") or lectura.get("rssi_proyectado_dbm")
        if bssid not in bssids_requeridos or punto_id is None or rssi is None:
            continue
        bssids_presentes.add(bssid)
        lecturas.append(
            {
                "punto_id": punto_id,
                "ssid": lectura.get("ssid") or conjunto.nombre,
                "bssid": bssid,
                "rssi": rssi,
                "canal": lectura.get("canal"),
                "frecuencia_mhz": lectura.get("frecuencia_mhz"),
                "modelo_origen": lectura.get("modelo_origen") or "rf-hibrido-1.2",
                "incertidumbre_db": lectura.get("incertidumbre_db") or 6.0,
            }
        )
    return lecturas if bssids_requeridos.issubset(bssids_presentes) else []


def _radio_principal(radios) -> dict:
    if isinstance(radios, dict):
        return radios
    if isinstance(radios, list):
        return next((radio for radio in radios if isinstance(radio, dict)), {})
    return {}


def _lecturas_proyectadas_ia_desde_items(conjunto, db: Session) -> list[dict]:
    puntos = MedicionRepository(db).listar_puntos_por_plano(plano_id=conjunto.plano_id)
    modelo = ModeloPropagacion()
    metros_por_pixel = conjunto.plano.escala_m_por_px or 1.0
    lecturas: list[dict] = []
    for item in conjunto.items:
        if item.pos_x is None or item.pos_y is None:
            continue
        radio_principal = _radio_principal(item.radios)
        banda = item.banda or conjunto.banda_objetivo or "5"
        for punto in puntos:
            rssi = modelo.predecir_rssi(
                distancia_px=math.hypot(
                    punto.pos_x - item.pos_x,
                    punto.pos_y - item.pos_y,
                ),
                metros_por_pixel=metros_por_pixel,
                banda=banda,
                potencia_dbm=radio_principal.get("potencia_dbm"),
                ganancia_dbi=radio_principal.get("ganancia_dbi", 2.14),
                perdida_cable_db=radio_principal.get("perdida_cable_db", 0.0),
            )
            lecturas.append(
                {
                    "punto_id": punto.id,
                    "ssid": item.ssid_snapshot or conjunto.nombre,
                    "bssid": item.bssid,
                    "rssi": rssi,
                    "canal": item.canal_snapshot,
                    "frecuencia_mhz": 2412 if banda == "2.4" else 5180,
                    "modelo_origen": "rf-hibrido-1.2",
                    "incertidumbre_db": 6.0,
                }
            )
    return lecturas


def _asegurar_lecturas_estimadas_ia(conjunto, db: Session) -> None:
    if conjunto.origen != "ia":
        return

    bssids_requeridos = {item.bssid.lower() for item in conjunto.items}
    med_repo = MedicionRepository(db)
    bssids_existentes = {
        ap["bssid"]
        for ap in med_repo.listar_aps_por_plano(
            plano_id=conjunto.plano_id,
            origen=ORIGEN_IA_ESTIMADA,
            conjunto_ap_id=conjunto.id,
        )
    }
    if bssids_requeridos.issubset(bssids_existentes):
        return

    lecturas = _lecturas_metricas_ia(conjunto, bssids_requeridos)
    if not lecturas:
        lecturas = _lecturas_proyectadas_ia_desde_items(conjunto, db)

    bssids_generados = {str(lectura["bssid"]).lower() for lectura in lecturas}
    if not bssids_requeridos.issubset(bssids_generados):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "No se pudieron reconstruir las lecturas estimadas de todos los APs "
                "recomendados por IA."
            ),
        )

    med_repo.reemplazar_lecturas_estimadas(
        conjunto_ap_id=conjunto.id,
        lecturas=lecturas,
    )
    conjunto.metricas_ia = {
        **(conjunto.metricas_ia or {}),
        "lecturas_estimadas": lecturas,
        "cantidad_lecturas_estimadas": len(lecturas),
        "lecturas_simuladas": lecturas,
        "cantidad_lecturas_simuladas": len(lecturas),
    }
    db.commit()
    db.refresh(conjunto)


def _metricas_ia_livianas(metricas: dict | None) -> dict | None:
    if not metricas:
        return metricas
    claves_pesadas = {
        "mapas_por_banda",
        "lecturas_estimadas",
        "lecturas_simuladas",
        "valores_proyectados",
    }
    return {
        clave: valor
        for clave, valor in metricas.items()
        if clave not in claves_pesadas
    }


def _conjunto_out(conjunto) -> ConjuntoAPOut:
    items = [
        ConjuntoAPItemOut(
            bssid=item.bssid,
            ssid=item.ssid_snapshot or "",
            canal=item.canal_snapshot,
            rssi_promedio=item.rssi_promedio_snapshot,
            pos_x=item.pos_x,
            pos_y=item.pos_y,
            accion_recomendada=item.accion_recomendada,
            justificacion=item.justificacion,
            altura_m=item.altura_m,
            tipo_montaje=item.tipo_montaje,
            banda=item.banda,
            modelo_ap=item.modelo_ap,
            costo_estimado=item.costo_estimado,
            radios=item.radios,
            **_metadata_potencia_tx(item.radios),
        )
        for item in conjunto.items
    ]
    return ConjuntoAPOut(
        id=conjunto.id,
        plano_id=conjunto.plano_id,
        conjunto_origen_id=conjunto.conjunto_origen_id,
        nombre=conjunto.nombre,
        proposito=conjunto.proposito,
        descripcion=conjunto.descripcion,
        es_principal=conjunto.es_principal,
        banda_objetivo=conjunto.banda_objetivo,
        origen=conjunto.origen,
        creado_por_id=conjunto.creado_por_id,
        resumen_ia=conjunto.resumen_ia,
        metricas_ia=_metricas_ia_livianas(conjunto.metricas_ia),
        restricciones_ia=conjunto.restricciones_ia,
        version_motor_ia=conjunto.version_motor_ia,
        cantidad_aps=len(items),
        items=items,
        created_at=conjunto.created_at,
        updated_at=conjunto.updated_at,
    )


def _verificar_ownership_conjunto(
    *,
    conjunto_id: int,
    current_user: Usuario,
    db: Session,
):
    conjunto = ConjuntoAPRepository(db).obtener_por_id(conjunto_id=conjunto_id)
    if conjunto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conjunto de APs no encontrado.",
        )
    _verificar_ownership_plano(
        plano_id=conjunto.plano_id,
        current_user=current_user,
        db=db,
    )
    return conjunto


def _firma_aps_interes(
    *,
    firma_base: str,
    aps_interes: list[dict],
    poligono_interes: list[dict] | None = None,
    conjunto_ap_id: int | None = None,
    modo_generacion: str = "SUBCONJUNTO",
) -> str:
    payload = {
        "modelo": "aps-interes-mediciones-v11-paleta-ekahau",
        "firma_base": firma_base,
        "conjunto_ap_id": conjunto_ap_id,
        "modo_generacion": modo_generacion,
        "poligono_interes": poligono_interes or [],
        "aps": [
            {
                "bssid": ap["bssid"],
                "pos_x": round(float(ap["pos_x"]), 2),
                "pos_y": round(float(ap["pos_y"]), 2),
            }
            for ap in aps_interes
        ],
    }
    serializado = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return f"aps:{hashlib.sha256(serializado.encode()).hexdigest()}"


def _requerir_poligono_interes(plano) -> list[dict]:
    poligono = plano.poligono_interes or []
    if len(poligono) < 3:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=("Debe definir un polígono de interés antes de generar heatmaps."),
        )
    return poligono


@router_planos_heatmap.get(
    "/{plano_id}/aps",
    response_model=list[APDisponibleOut],
    summary="Listar APs detectados del plano",
    description=(
        "Agrupa las mediciones por BSSID para que el técnico seleccione los APs "
        "de interés antes de generar mapas de calor."
    ),
)
def listar_aps_disponibles(
    plano_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[APDisponibleOut]:
    _verificar_ownership_plano(
        plano_id=plano_id,
        current_user=current_user,
        db=db,
    )
    aps = MedicionRepository(db).listar_aps_por_plano(plano_id=plano_id)
    mapas_recientes = MapaCalorRepository(db).listar_recientes_por_plano(
        plano_id=plano_id,
    )
    if mapas_recientes:
        ultimo_mapa = mapas_recientes[0]
        aps_ultimo_mapa = ultimo_mapa.aps_interes or [{"bssid": ultimo_mapa.bssid}]
    else:
        aps_ultimo_mapa = []
    bssids_ultimo_mapa = {ap["bssid"] for ap in aps_ultimo_mapa}
    posiciones_previas: dict[str, dict] = {}
    for mapa in mapas_recientes:
        for ap in mapa.aps_interes or []:
            posiciones_previas.setdefault(ap["bssid"], ap)
    for ap in aps:
        posicion = posiciones_previas.get(ap["bssid"])
        if posicion is None:
            continue
        ap["pos_x"] = posicion["pos_x"]
        ap["pos_y"] = posicion["pos_y"]
        ap["seleccionado"] = ap["bssid"] in bssids_ultimo_mapa
    return [APDisponibleOut(**ap) for ap in aps]


def _generar_heatmap_core(
    *,
    plano_id: int,
    request: Request,
    bssid: list[str],
    ap_pos_x: list[float] | None,
    ap_pos_y: list[float] | None,
    algoritmo: str,
    resolucion: int,
    db: Session,
    current_user: Usuario,
    conjunto_ap_id: int | None = None,
    modo_generacion: str | None = None,
    origen_lecturas: str = ORIGEN_CAMPO,
    conjunto_lecturas_id: int | None = None,
) -> MapaCalorOut:
    plano = _verificar_ownership_plano(
        plano_id=plano_id,
        current_user=current_user,
        db=db,
    )
    if not plano.calibrado:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El plano debe estar calibrado antes de generar el heatmap.",
        )
    poligono_interes = _requerir_poligono_interes(plano)

    med_repo = MedicionRepository(db)
    bssids_norm = _normalizar_bssids(bssid)
    if not bssids_norm:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe seleccionar al menos un AP de interés.",
        )
    aps_disponibles = med_repo.listar_aps_por_plano(
        plano_id=plano_id,
        origen=origen_lecturas,
        conjunto_ap_id=conjunto_lecturas_id,
    )
    aps_interes = _resolver_aps_interes(
        aps=aps_disponibles,
        bssids=bssids_norm,
        ap_pos_x=ap_pos_x,
        ap_pos_y=ap_pos_y,
    )

    puntos = med_repo.listar_puntos_rssi_heatmap(
        plano_id=plano_id,
        bssids=bssids_norm,
        origen=origen_lecturas,
        conjunto_ap_id=conjunto_lecturas_id,
    )
    if len(puntos) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Se requieren al menos 5 puntos de los APs seleccionados.",
        )

    algoritmo_norm = algoritmo.upper()
    modo_norm = modo_generacion or (
        "INDIVIDUAL" if len(bssids_norm) == 1 else "SUBCONJUNTO"
    )
    firma_base = med_repo.firma_mediciones_plano(
        plano_id=plano_id,
        bssids=bssids_norm,
        origen=origen_lecturas,
        conjunto_ap_id=conjunto_lecturas_id,
    )
    firma = _firma_aps_interes(
        firma_base=firma_base,
        aps_interes=aps_interes,
        poligono_interes=poligono_interes,
        conjunto_ap_id=conjunto_ap_id,
        modo_generacion=modo_norm,
    )
    mapa_repo = MapaCalorRepository(db)
    cache = mapa_repo.obtener_cache(
        plano_id=plano_id,
        algoritmo=algoritmo_norm,
        resolucion=resolucion,
        firma_mediciones=firma,
    )
    if cache is not None:
        return _mapa_out(cache, request, puntos=puntos)

    ap_principal = aps_interes[0]
    matriz = InterpolacionService().interpolar(
        puntos=puntos,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        resolucion=resolucion,
        algoritmo=algoritmo_norm,
    )
    mascara = mascara_poligono(
        poligono=poligono_interes,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        resolucion=resolucion,
    )
    png = HeatmapImageService().render_png(matriz, mascara=mascara)
    ruta = (
        f"heatmaps/{plano_id}/"
        f"{secrets.token_hex(8)}_{algoritmo_norm.lower()}_{resolucion}.png"
    )
    _storage().save(png, ruta)

    mapa = mapa_repo.crear(
        plano_id=plano_id,
        conjunto_ap_id=conjunto_ap_id,
        modo_generacion=modo_norm,
        algoritmo=algoritmo_norm,
        resolucion=resolucion,
        bssid=ap_principal["bssid"],
        ssid=ap_principal["ssid"],
        ap_pos_x=ap_principal["pos_x"],
        ap_pos_y=ap_principal["pos_y"],
        aps_interes=aps_interes,
        bssids_generacion=bssids_norm,
        matriz=matriz,
        escala=ESCALA_CWNA,
        ruta_imagen=ruta,
        cantidad_puntos=len(puntos),
        rssi_min=min(p.rssi for p in puntos),
        rssi_max=max(p.rssi for p in puntos),
        firma_mediciones=firma,
    )
    return _mapa_out(mapa, request, puntos=puntos)


@router_planos_heatmap.get(
    "/{plano_id}/heatmap",
    response_model=MapaCalorOut,
    summary="Generar mapa de calor",
    description=(
        "Genera o reutiliza el heatmap cacheado del plano mediante IDW. "
        "PB-05 — CA-1 a CA-6."
    ),
)
def generar_heatmap(
    plano_id: int,
    request: Request,
    bssid: list[str] = Query(..., description="BSSID de cada AP de interés"),
    ap_pos_x: list[float] | None = Query(
        default=None,
        description="Ubicación X confirmada de cada AP sobre el plano",
    ),
    ap_pos_y: list[float] | None = Query(
        default=None,
        description="Ubicación Y confirmada de cada AP sobre el plano",
    ),
    algoritmo: str = Query(default="IDW", pattern="^(IDW|idw)$"),
    resolucion: int = Query(default=128, enum=[64, 128, 256]),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> MapaCalorOut:
    return _generar_heatmap_core(
        plano_id=plano_id,
        request=request,
        bssid=bssid,
        ap_pos_x=ap_pos_x,
        ap_pos_y=ap_pos_y,
        algoritmo=algoritmo,
        resolucion=resolucion,
        db=db,
        current_user=current_user,
    )


@router_planos_heatmap.get(
    "/{plano_id}/mapas",
    response_model=list[MapaCalorOut],
    summary="Listar mapas de calor del plano",
)
def listar_mapas_plano(
    plano_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[MapaCalorOut]:
    _verificar_ownership_plano(plano_id=plano_id, current_user=current_user, db=db)
    mapas = MapaCalorRepository(db).listar_recientes_por_plano(plano_id=plano_id)
    return [_mapa_out(mapa, request) for mapa in mapas]


@router_planos_heatmap.get(
    "/{plano_id}/conjuntos-ap",
    response_model=list[ConjuntoAPOut],
    summary="Listar conjuntos de APs del plano",
)
def listar_conjuntos_ap(
    plano_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[ConjuntoAPOut]:
    _verificar_ownership_plano(
        plano_id=plano_id,
        current_user=current_user,
        db=db,
    )
    conjuntos = ConjuntoAPRepository(db).listar_por_plano(plano_id=plano_id)
    return [_conjunto_out(conjunto) for conjunto in conjuntos]


@router_planos_heatmap.post(
    "/{plano_id}/conjuntos-ap",
    response_model=ConjuntoAPOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear conjunto de APs del plano",
)
def crear_conjunto_ap(
    plano_id: int,
    body: ConjuntoAPCrearIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ConjuntoAPOut:
    _verificar_ownership_plano(
        plano_id=plano_id,
        current_user=current_user,
        db=db,
    )
    repo = ConjuntoAPRepository(db)
    nombre = body.nombre.strip()
    proposito = body.proposito.strip()
    if repo.existe_nombre(plano_id=plano_id, nombre=nombre):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un conjunto de APs con ese nombre en el plano.",
        )
    aps = MedicionRepository(db).listar_aps_por_plano(plano_id=plano_id)
    items = _resolver_items_conjunto(
        aps=aps,
        bssids=body.bssids,
        configuraciones_radio=body.configuraciones_radio,
    )
    _validar_banda_items(items=items, banda_objetivo=body.banda_objetivo)
    conjunto = repo.crear(
        plano_id=plano_id,
        nombre=nombre,
        proposito=proposito,
        descripcion=body.descripcion,
        es_principal=body.es_principal,
        banda_objetivo=body.banda_objetivo,
        items=items,
        origen="manual_web" if current_user.rol == "admin" else "manual_movil",
        creado_por_id=current_user.id,
    )
    return _conjunto_out(conjunto)


@router_conjuntos_ap.get(
    "/{conjunto_id}",
    response_model=ConjuntoAPOut,
    summary="Obtener conjunto de APs",
)
def obtener_conjunto_ap(
    conjunto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ConjuntoAPOut:
    conjunto = _verificar_ownership_conjunto(
        conjunto_id=conjunto_id,
        current_user=current_user,
        db=db,
    )
    return _conjunto_out(conjunto)


@router_conjuntos_ap.patch(
    "/{conjunto_id}",
    response_model=ConjuntoAPOut,
    summary="Actualizar conjunto de APs",
)
def actualizar_conjunto_ap(
    conjunto_id: int,
    body: ConjuntoAPActualizarIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ConjuntoAPOut:
    conjunto = _verificar_ownership_conjunto(
        conjunto_id=conjunto_id,
        current_user=current_user,
        db=db,
    )
    repo = ConjuntoAPRepository(db)
    nombre = body.nombre.strip() if body.nombre is not None else None
    if nombre is not None and repo.existe_nombre(
        plano_id=conjunto.plano_id,
        nombre=nombre,
        excluir_id=conjunto.id,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un conjunto de APs con ese nombre en el plano.",
        )
    items = None
    if body.bssids is not None:
        aps = MedicionRepository(db).listar_aps_por_plano(plano_id=conjunto.plano_id)
        items = _resolver_items_conjunto(
            aps=aps,
            bssids=body.bssids,
            configuraciones_radio=body.configuraciones_radio,
            items_existentes=list(conjunto.items),
        )
    elif body.configuraciones_radio is not None:
        aps = MedicionRepository(db).listar_aps_por_plano(plano_id=conjunto.plano_id)
        items = _resolver_items_conjunto(
            aps=aps,
            bssids=[item.bssid for item in conjunto.items],
            configuraciones_radio=body.configuraciones_radio,
            items_existentes=list(conjunto.items),
        )
    banda_objetivo = body.banda_objetivo or conjunto.banda_objetivo
    items_validacion = items or [
        {"bssid": item.bssid, "banda": item.banda} for item in conjunto.items
    ]
    _validar_banda_items(items=items_validacion, banda_objetivo=banda_objetivo)
    descripcion = (
        body.descripcion
        if "descripcion" in body.model_fields_set
        else conjunto.descripcion
    )
    actualizado = repo.actualizar(
        conjunto=conjunto,
        nombre=nombre,
        proposito=body.proposito.strip() if body.proposito is not None else None,
        descripcion=descripcion,
        es_principal=body.es_principal,
        banda_objetivo=body.banda_objetivo,
        items=items,
    )
    return _conjunto_out(actualizado)


@router_conjuntos_ap.delete(
    "/{conjunto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar conjunto de APs",
)
def eliminar_conjunto_ap(
    conjunto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> Response:
    conjunto = _verificar_ownership_conjunto(
        conjunto_id=conjunto_id,
        current_user=current_user,
        db=db,
    )
    rutas_mapas = [mapa.ruta_imagen for mapa in conjunto.mapas_calor]
    ConjuntoAPRepository(db).eliminar(conjunto=conjunto)
    storage = _storage()
    for ruta in rutas_mapas:
        storage.delete(ruta)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_conjuntos_ap.patch(
    "/{conjunto_id}/ubicacion-ap",
    response_model=ConjuntoAPOut,
    summary="Actualizar ubicación de un AP dentro del conjunto",
)
def actualizar_ubicacion_ap_conjunto(
    conjunto_id: int,
    body: ActualizarUbicacionAPConjuntoIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ConjuntoAPOut:
    conjunto = _verificar_ownership_conjunto(
        conjunto_id=conjunto_id,
        current_user=current_user,
        db=db,
    )
    repo = ConjuntoAPRepository(db)
    actualizado = repo.actualizar_ubicacion_ap(
        conjunto=conjunto,
        bssid=body.bssid.lower(),
        pos_x=body.pos_x,
        pos_y=body.pos_y,
    )
    if actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El AP no pertenece al conjunto.",
        )
    return _conjunto_out(actualizado)


@router_conjuntos_ap.post(
    "/{conjunto_id}/heatmaps",
    response_model=MapaCalorOut,
    summary="Generar heatmap desde conjunto de APs",
)
def generar_heatmap_conjunto(
    conjunto_id: int,
    body: GenerarHeatmapConjuntoIn,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> MapaCalorOut:
    conjunto = _verificar_ownership_conjunto(
        conjunto_id=conjunto_id,
        current_user=current_user,
        db=db,
    )
    _asegurar_lecturas_estimadas_ia(conjunto, db)
    bssids_conjunto = [item.bssid for item in conjunto.items]
    bssids_solicitados = _normalizar_bssids(body.bssids or [])
    if body.modo == "CONJUNTO_COMPLETO":
        bssids_generacion = bssids_conjunto
    elif body.modo == "INDIVIDUAL":
        if len(bssids_solicitados) != 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El modo INDIVIDUAL requiere exactamente un AP del conjunto.",
            )
        bssids_generacion = bssids_solicitados
    else:
        if not bssids_solicitados:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El modo SUBCONJUNTO requiere al menos un AP del conjunto.",
            )
        bssids_generacion = bssids_solicitados

    fuera_del_conjunto = [
        bssid for bssid in bssids_generacion if bssid not in bssids_conjunto
    ]
    if fuera_del_conjunto:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Uno o más APs seleccionados no pertenecen al conjunto.",
        )

    if (body.ap_pos_x is None) != (body.ap_pos_y is None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Las coordenadas X/Y de los APs del conjunto deben enviarse juntas.",
        )
    posiciones_request_completas = (
        body.ap_pos_x is not None
        and body.ap_pos_y is not None
        and len(body.ap_pos_x) == len(bssids_generacion)
        and len(body.ap_pos_y) == len(bssids_generacion)
    )
    if body.ap_pos_x is not None and not posiciones_request_completas:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La cantidad de coordenadas no coincide con los APs seleccionados.",
        )
    if posiciones_request_completas:
        ap_pos_x = body.ap_pos_x
        ap_pos_y = body.ap_pos_y
    else:
        items_por_bssid = {item.bssid: item for item in conjunto.items}
        ap_pos_x = [
            items_por_bssid[bssid].pos_x
            for bssid in bssids_generacion
            if items_por_bssid[bssid].pos_x is not None
        ]
        ap_pos_y = [
            items_por_bssid[bssid].pos_y
            for bssid in bssids_generacion
            if items_por_bssid[bssid].pos_y is not None
        ]
    posiciones_completas = len(ap_pos_x) == len(bssids_generacion) and len(
        ap_pos_y
    ) == len(bssids_generacion)

    origen_lecturas = ORIGEN_IA_ESTIMADA if conjunto.origen == "ia" else ORIGEN_CAMPO
    conjunto_lecturas_id = conjunto.id if conjunto.origen == "ia" else None

    return _generar_heatmap_core(
        plano_id=conjunto.plano_id,
        request=request,
        bssid=bssids_generacion,
        ap_pos_x=ap_pos_x if posiciones_completas else None,
        ap_pos_y=ap_pos_y if posiciones_completas else None,
        algoritmo=body.algoritmo,
        resolucion=body.resolucion,
        db=db,
        current_user=current_user,
        conjunto_ap_id=conjunto.id,
        modo_generacion=body.modo,
        origen_lecturas=origen_lecturas,
        conjunto_lecturas_id=conjunto_lecturas_id,
    )


@router_conjuntos_ap.post(
    "/{conjunto_id}/heatmaps/combinaciones-faltantes",
    response_model=list[MapaCalorResumenOut],
    summary="Generar o actualizar heatmaps objetivo del conjunto",
)
def generar_heatmaps_faltantes_conjunto(
    conjunto_id: int,
    body: GenerarHeatmapsFaltantesIn,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> list[MapaCalorResumenOut]:
    conjunto = _verificar_ownership_conjunto(
        conjunto_id=conjunto_id,
        current_user=current_user,
        db=db,
    )
    _asegurar_lecturas_estimadas_ia(conjunto, db)
    bssids_conjunto = [item.bssid for item in conjunto.items]
    if not bssids_conjunto:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El conjunto no tiene APs para generar mapas de calor.",
        )

    algoritmos = _algoritmos_faltantes(body)
    mapas_objetivo = _mapas_objetivo_conjunto(
        bssids=bssids_conjunto,
        origen_conjunto=conjunto.origen,
    )
    if not mapas_objetivo:
        return []

    items_por_bssid = {item.bssid: item for item in conjunto.items}
    origen_lecturas = ORIGEN_IA_ESTIMADA if conjunto.origen == "ia" else ORIGEN_CAMPO
    conjunto_lecturas_id = conjunto.id if conjunto.origen == "ia" else None
    mapas_generados: list[MapaCalorResumenOut] = []
    mapas_existentes = MapaCalorRepository(db).listar_recientes_por_plano(
        plano_id=conjunto.plano_id,
    )
    mapas_reemplazados_por_clave: dict[tuple[str, tuple[str, ...]], list[int]] = {}
    reemplazos_mapa_id: dict[int, int] = {}
    if body.reemplazar_existentes:
        for mapa_existente in [
            mapa for mapa in mapas_existentes if mapa.conjunto_ap_id == conjunto.id
        ]:
            clave_publicacion = _clave_publicacion_mapa(mapa_existente)
            mapas_reemplazados_por_clave.setdefault(clave_publicacion, []).append(
                mapa_existente.id
            )
            db.delete(mapa_existente)
        db.commit()
        mapas_existentes = [
            mapa for mapa in mapas_existentes if mapa.conjunto_ap_id != conjunto.id
        ]
    for algoritmo_norm in algoritmos:
        existentes = {
            _clave_bssids(mapa.bssids_generacion or [mapa.bssid]): mapa
            for mapa in mapas_existentes
            if mapa.conjunto_ap_id == conjunto.id
            and mapa.algoritmo.upper() == algoritmo_norm
            and mapa.resolucion == body.resolucion
        }
        mapas_a_generar = (
            mapas_objetivo
            if body.actualizar_existentes or body.reemplazar_existentes
            else [
                (bssids_mapa, modo_mapa)
                for bssids_mapa, modo_mapa in mapas_objetivo
                if _clave_bssids(bssids_mapa) not in existentes
            ]
        )
        for bssids_mapa, modo_mapa in mapas_a_generar:
            clave_mapa = _clave_bssids(bssids_mapa)
            if body.actualizar_existentes and not body.reemplazar_existentes:
                for mapa_existente in [
                    mapa
                    for mapa in mapas_existentes
                    if mapa.conjunto_ap_id == conjunto.id
                    and mapa.algoritmo.upper() == algoritmo_norm
                    and mapa.resolucion == body.resolucion
                    and _clave_bssids(mapa.bssids_generacion or [mapa.bssid])
                    == clave_mapa
                ]:
                    clave_publicacion = _clave_publicacion_mapa(mapa_existente)
                    mapas_reemplazados_por_clave.setdefault(
                        clave_publicacion,
                        [],
                    ).append(mapa_existente.id)
                    db.delete(mapa_existente)
                db.commit()
            ap_pos_x = [
                float(items_por_bssid[bssid].pos_x)
                for bssid in bssids_mapa
                if items_por_bssid[bssid].pos_x is not None
            ]
            ap_pos_y = [
                float(items_por_bssid[bssid].pos_y)
                for bssid in bssids_mapa
                if items_por_bssid[bssid].pos_y is not None
            ]
            posiciones_completas = len(ap_pos_x) == len(bssids_mapa) and len(
                ap_pos_y
            ) == len(bssids_mapa)
            mapa = _generar_heatmap_core(
                plano_id=conjunto.plano_id,
                request=request,
                bssid=bssids_mapa,
                ap_pos_x=ap_pos_x if posiciones_completas else None,
                ap_pos_y=ap_pos_y if posiciones_completas else None,
                algoritmo=algoritmo_norm,
                resolucion=body.resolucion,
                db=db,
                current_user=current_user,
                conjunto_ap_id=conjunto.id,
                modo_generacion=modo_mapa,
                origen_lecturas=origen_lecturas,
                conjunto_lecturas_id=conjunto_lecturas_id,
            )
            clave_generada = _clave_publicacion_mapa(mapa)
            for mapa_reemplazado_id in mapas_reemplazados_por_clave.get(
                clave_generada,
                [],
            ):
                reemplazos_mapa_id[mapa_reemplazado_id] = mapa.id
            mapas_generados.append(_mapa_resumen_desde_out(mapa))
    if reemplazos_mapa_id or mapas_generados:
        _actualizar_enlaces_cliente_por_reemplazo_mapas(
            db=db,
            proyecto_id=conjunto.plano.proyecto_id,
            reemplazos_mapa_id=reemplazos_mapa_id,
            conjunto_id=conjunto.id,
            nuevos_mapa_ids=[mapa.id for mapa in mapas_generados],
        )
    return mapas_generados


@router_mapas.get(
    "/archivo/{ruta:path}",
    summary="Descargar imagen de heatmap (URL firmada)",
)
def descargar_imagen_heatmap(
    ruta: str,
    exp: int = Query(...),
    sig: str = Query(...),
    db: Session = Depends(get_db),
) -> Response:
    if not verificar_firma(
        ruta_relativa=ruta,
        secret=settings.storage_url_secret,
        exp=exp,
        sig=sig,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Firma inválida o URL expirada.",
        )

    mapa = MapaCalorRepository(db).obtener_por_ruta(ruta_imagen=ruta)
    if mapa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mapa de calor no encontrado.",
        )
    storage = _storage()
    if not storage.exists(ruta):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada en storage.",
        )
    media_type = (
        "image/png"
        if Path(ruta).suffix.lower() == ".png"
        else "application/octet-stream"
    )
    return Response(content=storage.read(ruta), media_type=media_type)


@router_mapas.delete(
    "/{mapa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar mapa de calor",
)
def eliminar_mapa_calor(
    mapa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> Response:
    mapa = _verificar_ownership_mapa(
        mapa_id=mapa_id,
        current_user=current_user,
        db=db,
    )
    ruta_imagen = mapa.ruta_imagen
    MapaCalorRepository(db).eliminar(mapa=mapa)
    _storage().delete(ruta_imagen)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
