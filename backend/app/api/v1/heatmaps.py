"""Endpoints de heatmap y análisis de cobertura.

Sprint 4 — PB-05 (Generar mapa de calor), PB-06 (Analizar cobertura).
"""

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
    return MapaCalorOut(
        id=mapa.id,
        plano_id=mapa.plano_id,
        algoritmo=mapa.algoritmo,
        resolucion=mapa.resolucion,
        bssid=mapa.bssid,
        ssid=mapa.ssid,
        ap_pos_x=mapa.ap_pos_x,
        ap_pos_y=mapa.ap_pos_y,
        url_imagen=_firmar(mapa.ruta_imagen, request),
        matriz=mapa.matriz,
        escala=mapa.escala,
        cantidad_puntos=mapa.cantidad_puntos,
        rssi_min=mapa.rssi_min,
        rssi_max=mapa.rssi_max,
        created_at=mapa.created_at,
    )


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
    bssid: str = Query(..., description="BSSID del AP de interés"),
    ap_pos_x: float | None = Query(
        default=None,
        ge=0,
        description="Ubicación X confirmada del AP sobre el plano",
    ),
    ap_pos_y: float | None = Query(
        default=None,
        ge=0,
        description="Ubicación Y confirmada del AP sobre el plano",
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
    bssid_norm = bssid.lower()
    ap = med_repo.obtener_ap_por_bssid(plano_id=plano_id, bssid=bssid_norm)
    if ap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AP no encontrado en las mediciones del plano.",
        )

    puntos = med_repo.listar_puntos_rssi_heatmap(
        plano_id=plano_id,
        bssid=bssid_norm,
    )
    if len(puntos) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Se requieren al menos 5 puntos del AP seleccionado.",
        )

    algoritmo_norm = algoritmo.upper()
    ap_x = ap_pos_x if ap_pos_x is not None else ap["pos_x"]
    ap_y = ap_pos_y if ap_pos_y is not None else ap["pos_y"]
    firma_base = med_repo.firma_mediciones_plano(
        plano_id=plano_id,
        bssid=bssid_norm,
    )
    firma = f"{bssid_norm}:{firma_base}:{ap_x:.2f}:{ap_y:.2f}"
    mapa_repo = MapaCalorRepository(db)
    cache = mapa_repo.obtener_cache(
        plano_id=plano_id,
        algoritmo=algoritmo_norm,
        resolucion=resolucion,
        firma_mediciones=firma,
    )
    if cache is not None:
        return _mapa_out(cache, request)

    matriz = InterpolacionService().interpolar(
        puntos=puntos,
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
        bssid=bssid_norm,
        ssid=ap["ssid"],
        ap_pos_x=ap_x,
        ap_pos_y=ap_y,
        matriz=matriz,
        escala=ESCALA_CWNA,
        ruta_imagen=ruta,
        cantidad_puntos=len(puntos),
        rssi_min=min(p.rssi for p in puntos),
        rssi_max=max(p.rssi for p in puntos),
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
    mediciones = MedicionRepository(db).listar_mediciones_por_plano(
        plano_id=mapa.plano_id,
    )
    datos = AnalisisCoberturaService().analizar(
        matriz=mapa.matriz,
        mediciones=mediciones,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        ap_referencia={
            "bssid": mapa.bssid,
            "pos_x": mapa.ap_pos_x,
            "pos_y": mapa.ap_pos_y,
        },
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
