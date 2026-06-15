"""Endpoints de heatmap y análisis de cobertura.

Sprint 4 — PB-05 (Generar mapa de calor), PB-06 (Analizar cobertura).
"""

import hashlib
import json
import secrets
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.heatmap import MapaCalor
from app.models.usuario import Usuario
from app.repositories.heatmap_repository import (
    AnalisisCoberturaRepository,
    MapaCalorRepository,
)
from app.repositories.medicion_repository import MedicionRepository
from app.repositories.plano_repository import PlanoRepository
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.heatmap import (
    AnalisisCoberturaOut,
    APDetectadoOut,
    APDisponibleOut,
    ConfirmarAPIn,
    MapaCalorOut,
)
from app.services.analisis_cobertura_service import AnalisisCoberturaService
from app.services.interpolacion_service import (
    ESCALA_CWNA,
    HeatmapImageService,
    InterpolacionService,
    PuntoRSSI,
)
from app.storage import LocalFilesystemStorage, generar_url_firmada, verificar_firma

router_planos_heatmap = APIRouter(prefix="/planos", tags=["heatmaps"])
router_mapas = APIRouter(prefix="/mapas", tags=["heatmaps"])
router_aps = APIRouter(prefix="/aps", tags=["heatmaps"])


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
    proyecto = ProyectoRepository(db).obtener_por_id(
        proyecto_id=plano.proyecto_id,
        tecnico_id=current_user.id,
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


def _mapa_out(mapa: MapaCalor, request: Request) -> MapaCalorOut:
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
    return MapaCalorOut(
        id=mapa.id,
        plano_id=mapa.plano_id,
        algoritmo=mapa.algoritmo,
        resolucion=mapa.resolucion,
        bssid=mapa.bssid,
        ssid=mapa.ssid,
        ap_pos_x=mapa.ap_pos_x,
        ap_pos_y=mapa.ap_pos_y,
        aps_interes=aps_interes,
        url_imagen=_firmar(mapa.ruta_imagen, request),
        matriz=mapa.matriz,
        escala=mapa.escala,
        cantidad_puntos=mapa.cantidad_puntos,
        rssi_min=mapa.rssi_min,
        rssi_max=mapa.rssi_max,
        created_at=mapa.created_at,
    )


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


def _firma_aps_interes(*, firma_base: str, aps_interes: list[dict]) -> str:
    payload = {
        "modelo": "aps-interes-anclas-v2",
        "firma_base": firma_base,
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


def _agregar_anclas_aps(
    *,
    puntos: list[PuntoRSSI],
    aps_interes: list[dict],
    rssi_maximos: dict[str, float],
) -> list[PuntoRSSI]:
    puntos_interpolacion = list(puntos)
    for idx, ap in enumerate(aps_interes):
        rssi_observado = rssi_maximos.get(
            ap["bssid"],
            float(ap["rssi_promedio"]),
        )
        puntos_interpolacion.append(
            PuntoRSSI(
                punto_id=-(idx + 1),
                x=float(ap["pos_x"]),
                y=float(ap["pos_y"]),
                rssi=max(rssi_observado, -50.0),
            )
        )
    return puntos_interpolacion


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
    return [APDisponibleOut(**ap) for ap in aps]


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
    algoritmo: str = Query(default="IDW", pattern="^(IDW|KRIGING|idw|kriging)$"),
    resolucion: int = Query(default=128, enum=[64, 128, 256]),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
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

    med_repo = MedicionRepository(db)
    bssids_norm = _normalizar_bssids(bssid)
    if not bssids_norm:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe seleccionar al menos un AP de interés.",
        )
    aps_disponibles = med_repo.listar_aps_por_plano(plano_id=plano_id)
    aps_interes = _resolver_aps_interes(
        aps=aps_disponibles,
        bssids=bssids_norm,
        ap_pos_x=ap_pos_x,
        ap_pos_y=ap_pos_y,
    )

    puntos = med_repo.listar_puntos_rssi_heatmap(
        plano_id=plano_id,
        bssids=bssids_norm,
    )
    if len(puntos) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Se requieren al menos 5 puntos de los APs seleccionados.",
        )

    algoritmo_norm = algoritmo.upper()
    firma_base = med_repo.firma_mediciones_plano(
        plano_id=plano_id,
        bssids=bssids_norm,
    )
    firma = _firma_aps_interes(
        firma_base=firma_base,
        aps_interes=aps_interes,
    )
    mapa_repo = MapaCalorRepository(db)
    cache = mapa_repo.obtener_cache(
        plano_id=plano_id,
        algoritmo=algoritmo_norm,
        resolucion=resolucion,
        firma_mediciones=firma,
    )
    if cache is not None:
        return _mapa_out(cache, request)

    ap_principal = aps_interes[0]
    rssi_maximos = med_repo.rssi_maximo_por_bssid(
        plano_id=plano_id,
        bssids=bssids_norm,
    )
    puntos_interpolacion = _agregar_anclas_aps(
        puntos=puntos,
        aps_interes=aps_interes,
        rssi_maximos=rssi_maximos,
    )
    matriz = InterpolacionService().interpolar(
        puntos=puntos_interpolacion,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        resolucion=resolucion,
        algoritmo=algoritmo_norm,
    )
    png = HeatmapImageService().render_png(matriz)
    ruta = (
        f"heatmaps/{plano_id}/"
        f"{secrets.token_hex(8)}_{algoritmo_norm.lower()}_{resolucion}.png"
    )
    _storage().save(png, ruta)

    mapa = mapa_repo.crear(
        plano_id=plano_id,
        algoritmo=algoritmo_norm,
        resolucion=resolucion,
        bssid=ap_principal["bssid"],
        ssid=ap_principal["ssid"],
        ap_pos_x=ap_principal["pos_x"],
        ap_pos_y=ap_principal["pos_y"],
        aps_interes=aps_interes,
        matriz=matriz,
        escala=ESCALA_CWNA,
        ruta_imagen=ruta,
        cantidad_puntos=len(puntos),
        rssi_min=min(p.rssi for p in puntos_interpolacion),
        rssi_max=max(p.rssi for p in puntos_interpolacion),
        firma_mediciones=firma,
    )
    return _mapa_out(mapa, request)


@router_mapas.post(
    "/{mapa_id}/analisis",
    response_model=AnalisisCoberturaOut,
    summary="Analizar cobertura del mapa",
    description="Regenera de forma idempotente el análisis automático. PB-06.",
)
def analizar_mapa(
    mapa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> AnalisisCoberturaOut:
    mapa = _verificar_ownership_mapa(
        mapa_id=mapa_id,
        current_user=current_user,
        db=db,
    )
    plano = mapa.plano
    aps_referencia = mapa.aps_interes or [
        {
            "bssid": mapa.bssid,
            "pos_x": mapa.ap_pos_x,
            "pos_y": mapa.ap_pos_y,
        }
    ]
    bssids_interes = {ap["bssid"] for ap in aps_referencia}
    mediciones = [
        medicion
        for medicion in MedicionRepository(db).listar_mediciones_por_plano(
            plano_id=mapa.plano_id,
        )
        if medicion.bssid in bssids_interes
    ]
    datos = AnalisisCoberturaService().analizar(
        matriz=mapa.matriz,
        mediciones=mediciones,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        aps_referencia=aps_referencia,
    )
    analisis = AnalisisCoberturaRepository(db).reemplazar(
        mapa=mapa,
        pct_cobertura=datos["pct_cobertura"],
        pct_zonas_muertas=datos["pct_zonas_muertas"],
        celdas_zonas_muertas=datos["celdas_zonas_muertas"],
        cantidad_solapamientos=datos["cantidad_solapamientos"],
        cantidad_interferencias=datos["cantidad_interferencias"],
        hallazgos=datos["hallazgos"],
        resumen=datos["resumen"],
        aps_detectados=datos["aps_detectados"],
    )
    return AnalisisCoberturaOut.model_validate(analisis)


@router_aps.patch(
    "/{ap_id}",
    response_model=APDetectadoOut,
    summary="Confirmar ubicación estimada de AP",
)
def confirmar_ap(
    ap_id: int,
    body: ConfirmarAPIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> APDetectadoOut:
    repo = AnalisisCoberturaRepository(db)
    ap = repo.obtener_ap_por_id(ap_id=ap_id)
    if ap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AP detectado no encontrado.",
        )
    _verificar_ownership_mapa(
        mapa_id=ap.analisis.mapa_calor_id,
        current_user=current_user,
        db=db,
    )
    actualizado = repo.confirmar_ap(
        ap=ap,
        pos_x=body.pos_x,
        pos_y=body.pos_y,
        confirmado=body.confirmado,
    )
    return APDetectadoOut.model_validate(actualizado)


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
