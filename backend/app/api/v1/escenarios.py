"""Endpoints Sprint 5: IA, comparación y reportes."""

from __future__ import annotations

import hashlib
import secrets
from pathlib import Path
from urllib.parse import unquote

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.ai.optimizador_ap_service import OptimizadorAPService
from app.api.v1.heatmaps import _mapa_out
from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.escenario import EscenarioOptimizado, Reporte
from app.models.heatmap import MapaCalor
from app.models.plano import Plano
from app.models.proyecto import Proyecto
from app.models.usuario import Usuario
from app.repositories.escenario_repository import EscenarioRepository, ReporteRepository
from app.repositories.heatmap_repository import MapaCalorRepository
from app.repositories.medicion_repository import MedicionRepository
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.escenario import (
    ComparacionEscenarioOut,
    EscenarioOptimizadoOut,
    EscenariosGeneradosOut,
    ReporteCrearIn,
    ReporteOut,
    ResumenComparacionOut,
    RestriccionesEscenarioIn,
)
from app.services.interpolacion_service import (
    ESCALA_CWNA,
    HeatmapImageService,
    InterpolacionService,
    PuntoRSSI,
)
from app.services.reporte_service import ReporteService
from app.storage import LocalFilesystemStorage, generar_url_firmada, verificar_firma

router_proyectos_escenarios = APIRouter(prefix="/proyectos", tags=["escenarios"])
router_escenarios = APIRouter(prefix="/escenarios", tags=["escenarios"])
router_reportes = APIRouter(prefix="/reportes", tags=["reportes"])


def _storage() -> LocalFilesystemStorage:
    return LocalFilesystemStorage(root=settings.storage_root)


def _firmar_descarga(ruta: str) -> str:
    return generar_url_firmada(
        ruta_relativa=ruta,
        secret=settings.storage_url_secret,
        base_url=settings.public_api_url,
        ttl_seconds=24 * 3600,
    ).replace("/planos/archivo/", "/reportes/archivo/", 1)


def _proyecto_tecnico(
    *,
    proyecto_id: int,
    current_user: Usuario,
    db: Session,
) -> Proyecto:
    proyecto = ProyectoRepository(db).obtener_por_id(
        proyecto_id=proyecto_id,
        tecnico_id=current_user.id,
    )
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return proyecto


def _escenario_tecnico(
    *,
    escenario_id: int,
    current_user: Usuario,
    db: Session,
) -> EscenarioOptimizado:
    escenario = EscenarioRepository(db).obtener_por_id(escenario_id=escenario_id)
    if escenario is None:
        raise HTTPException(status_code=404, detail="Escenario no encontrado.")
    _proyecto_tecnico(
        proyecto_id=escenario.proyecto_id,
        current_user=current_user,
        db=db,
    )
    return escenario


def _reporte_tecnico(
    *,
    reporte_id: int,
    current_user: Usuario,
    db: Session,
) -> Reporte:
    reporte = ReporteRepository(db).obtener_por_id(reporte_id=reporte_id)
    if reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado.")
    _proyecto_tecnico(
        proyecto_id=reporte.proyecto_id,
        current_user=current_user,
        db=db,
    )
    return reporte


def _plano_base(proyecto: Proyecto) -> Plano:
    planos = sorted(proyecto.planos, key=lambda p: p.created_at or p.id, reverse=True)
    plano = next((p for p in planos if p.calibrado), None)
    if plano is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El proyecto requiere al menos un plano calibrado.",
        )
    return plano


def _mapa_actual(
    *,
    plano: Plano,
    db: Session,
) -> tuple[MapaCalor, list[PuntoRSSI]]:
    mapa_repo = MapaCalorRepository(db)
    med_repo = MedicionRepository(db)
    mapa = next(
        (
            item
            for item in mapa_repo.listar_recientes_por_plano(plano_id=plano.id)
            if item.modo_generacion != "PROYECTADO"
        ),
        None,
    )
    bssids = [
        ap["bssid"]
        for ap in med_repo.listar_aps_por_plano(plano_id=plano.id)
    ]
    if not bssids:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No hay APs medidos para generar escenarios.",
        )
    puntos = med_repo.listar_puntos_rssi_heatmap(plano_id=plano.id, bssids=bssids)
    if len(puntos) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Se requieren al menos 5 puntos de medición para IA.",
        )
    if mapa is not None:
        return mapa, puntos

    matriz = InterpolacionService().interpolar(
        puntos=puntos,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        resolucion=64,
        algoritmo="IDW",
    )
    ruta = f"heatmaps/sp5_actual_{plano.id}_{secrets.token_hex(8)}.png"
    _storage().save(HeatmapImageService().render_png(matriz), ruta)
    firma = hashlib.sha1(
        f"sp5-actual:{plano.id}:{med_repo.firma_mediciones_plano(plano_id=plano.id)}".encode(),
        usedforsecurity=False,
    ).hexdigest()
    aps = med_repo.listar_aps_por_plano(plano_id=plano.id)
    mapa = mapa_repo.crear(
        plano_id=plano.id,
        modo_generacion="SUBCONJUNTO",
        algoritmo="IDW",
        resolucion=64,
        bssid=aps[0]["bssid"],
        ssid=aps[0]["ssid"],
        ap_pos_x=aps[0]["pos_x"],
        ap_pos_y=aps[0]["pos_y"],
        aps_interes=aps,
        bssids_generacion=bssids,
        matriz=matriz,
        escala=ESCALA_CWNA,
        ruta_imagen=ruta,
        cantidad_puntos=len(puntos),
        rssi_min=min(min(fila) for fila in matriz),
        rssi_max=max(max(fila) for fila in matriz),
        firma_mediciones=firma,
    )
    return mapa, puntos


@router_proyectos_escenarios.post(
    "/{proyecto_id}/escenarios",
    response_model=EscenariosGeneradosOut,
    status_code=status.HTTP_201_CREATED,
)
def generar_escenarios(
    proyecto_id: int,
    body: RestriccionesEscenarioIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> EscenariosGeneradosOut:
    proyecto = _proyecto_tecnico(proyecto_id=proyecto_id, current_user=current_user, db=db)
    plano = _plano_base(proyecto)
    mapa_actual, puntos = _mapa_actual(plano=plano, db=db)
    optimizador = OptimizadorAPService()
    alternativas = optimizador.optimizar(
        puntos_actuales=puntos,
        matriz_actual=mapa_actual.matriz,
        ancho_px=plano.ancho_px,
        alto_px=plano.alto_px,
        metros_por_pixel=plano.escala_m_por_px or 1.0,
        max_aps=body.max_aps,
        presupuesto=body.presupuesto,
        banda=body.banda_preferida,
        modelo_ap=body.modelo_ap,
        costo_unitario=body.costo_unitario,
        resolucion=body.resolucion,
    )
    mapa_repo = MapaCalorRepository(db)
    escenario_repo = EscenarioRepository(db)
    escenarios: list[EscenarioOptimizado] = []
    for idx, alternativa in enumerate(alternativas, start=1):
        ruta = f"heatmaps/sp5_proyectado_{proyecto.id}_{idx}_{secrets.token_hex(8)}.png"
        _storage().save(HeatmapImageService().render_png(alternativa.matriz), ruta)
        firma = hashlib.sha1(
            f"sp5-proyectado:{proyecto.id}:{idx}:{secrets.token_hex(8)}".encode(),
            usedforsecurity=False,
        ).hexdigest()
        mapa_proyectado = mapa_repo.crear(
            plano_id=plano.id,
            modo_generacion="PROYECTADO",
            algoritmo="FSPL",
            resolucion=body.resolucion,
            bssid=f"sp5:{idx:02d}:00:00:00",
            ssid=alternativa.nombre,
            ap_pos_x=alternativa.recomendaciones[0]["coord_x"],
            ap_pos_y=alternativa.recomendaciones[0]["coord_y"],
            aps_interes=[
                {
                    "bssid": f"sp5:{idx:02d}:{rec_idx:02d}:00:00",
                    "ssid": rec["modelo_ap"],
                    "canal": None,
                    "frecuencia_mhz": None,
                    "rssi_promedio": rec["rssi_proyectado"],
                    "pos_x": rec["coord_x"],
                    "pos_y": rec["coord_y"],
                    "cantidad_puntos": len(puntos),
                }
                for rec_idx, rec in enumerate(alternativa.recomendaciones, start=1)
            ],
            bssids_generacion=[
                f"sp5:{idx:02d}:{rec_idx:02d}:00:00"
                for rec_idx, _ in enumerate(alternativa.recomendaciones, start=1)
            ],
            matriz=alternativa.matriz,
            escala=ESCALA_CWNA,
            ruta_imagen=ruta,
            cantidad_puntos=len(puntos),
            rssi_min=min(min(fila) for fila in alternativa.matriz),
            rssi_max=max(max(fila) for fila in alternativa.matriz),
            firma_mediciones=firma,
        )
        escenario = escenario_repo.crear(
            proyecto_id=proyecto.id,
            plano_id=plano.id,
            mapa_actual_id=mapa_actual.id,
            mapa_proyectado_id=mapa_proyectado.id,
            nombre=alternativa.nombre,
            banda=alternativa.banda,
            modelo_ap=alternativa.modelo_ap,
            pct_cobertura_actual=alternativa.pct_cobertura_actual,
            pct_cobertura=alternativa.pct_cobertura,
            costo_estimado=alternativa.costo_estimado,
            cantidad_aps=alternativa.cantidad_aps,
            resumen=alternativa.resumen,
            restricciones=body.model_dump(),
            metricas=alternativa.metricas,
            recomendaciones=alternativa.recomendaciones,
        )
        escenarios.append(escenario)
    return EscenariosGeneradosOut(
        escenarios=[EscenarioOptimizadoOut.model_validate(e) for e in escenarios]
    )


@router_escenarios.get("/{escenario_id}/comparacion", response_model=ComparacionEscenarioOut)
def comparar_escenario(
    escenario_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ComparacionEscenarioOut:
    escenario = _escenario_tecnico(escenario_id=escenario_id, current_user=current_user, db=db)
    if escenario.mapa_actual is None or escenario.mapa_proyectado is None:
        raise HTTPException(status_code=409, detail="El escenario no tiene mapas asociados.")
    actual = escenario.mapa_actual.matriz
    proyectado = escenario.mapa_proyectado.matriz
    filas = min(len(actual), len(proyectado))
    cols = min(len(actual[0]), len(proyectado[0])) if filas else 0
    diferencia = [
        [round(proyectado[y][x] - actual[y][x], 2) for x in range(cols)]
        for y in range(filas)
    ]
    delta_muertas = _contar_zonas_muertas(proyectado) - _contar_zonas_muertas(actual)
    return ComparacionEscenarioOut(
        escenario=EscenarioOptimizadoOut.model_validate(escenario),
        heatmap_actual=_mapa_out(escenario.mapa_actual, request),
        heatmap_proyectado=_mapa_out(escenario.mapa_proyectado, request),
        matriz_diferencia=diferencia,
        resumen=ResumenComparacionOut(
            delta_pct_cobertura=round(
                escenario.pct_cobertura - escenario.pct_cobertura_actual,
                2,
            ),
            delta_zonas_muertas=delta_muertas,
            costo_estimado=escenario.costo_estimado,
            cantidad_cambios=len(escenario.recomendaciones),
            lectura="verde = mejora RSSI, rojo = degradacion",
        ),
    )


@router_proyectos_escenarios.post("/{proyecto_id}/reportes", response_model=ReporteOut, status_code=201)
def crear_reporte(
    proyecto_id: int,
    body: ReporteCrearIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ReporteOut:
    proyecto = _proyecto_tecnico(proyecto_id=proyecto_id, current_user=current_user, db=db)
    escenario = None
    if body.escenario_id is not None:
        escenario = _escenario_tecnico(
            escenario_id=body.escenario_id,
            current_user=current_user,
            db=db,
        )
    repo = ReporteRepository(db)
    reporte = repo.crear_procesando(proyecto_id=proyecto.id, escenario_id=body.escenario_id)
    try:
        escenarios = EscenarioRepository(db).listar_por_proyecto(proyecto_id=proyecto.id)
        cantidad_mediciones = sum(len(p.mediciones) for plano in proyecto.planos for p in plano.puntos_medicion)
        generado = ReporteService().generar(
            proyecto=proyecto,
            escenarios=escenarios,
            escenario_seleccionado=escenario,
            cantidad_mediciones=cantidad_mediciones,
        )
        ruta = f"reportes/proyecto_{proyecto.id}/reporte_{reporte.id}.pdf"
        _storage().save(generado.contenido, ruta)
        reporte = repo.marcar_listo(
            reporte=reporte,
            ruta_pdf=ruta,
            sha256=generado.sha256,
            tamanio_bytes=generado.tamanio_bytes,
        )
    except Exception as exc:
        reporte = repo.marcar_error(reporte=reporte, error=str(exc))
    return _reporte_out(reporte)


@router_reportes.get("/archivo/{ruta:path}")
def descargar_reporte_firmado(
    ruta: str,
    exp: int = Query(...),
    sig: str = Query(...),
) -> Response:
    ruta_relativa = unquote(ruta)
    if not ruta_relativa.startswith("reportes/"):
        raise HTTPException(status_code=404, detail="Reporte no encontrado.")
    if not verificar_firma(
        ruta_relativa=ruta_relativa,
        secret=settings.storage_url_secret,
        exp=exp,
        sig=sig,
    ):
        raise HTTPException(status_code=403, detail="URL expirada o invalida.")
    storage = _storage()
    if not storage.exists(ruta_relativa):
        raise HTTPException(status_code=404, detail="Reporte no encontrado.")
    return Response(
        content=storage.read(ruta_relativa),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{Path(ruta_relativa).name}"'},
    )


@router_reportes.get("/{reporte_id}", response_model=ReporteOut)
def obtener_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> ReporteOut:
    reporte = _reporte_tecnico(reporte_id=reporte_id, current_user=current_user, db=db)
    return _reporte_out(reporte)


@router_reportes.get("/{reporte_id}/descargar")
def descargar_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> Response:
    reporte = _reporte_tecnico(reporte_id=reporte_id, current_user=current_user, db=db)
    if reporte.estado != "LISTO" or not reporte.ruta_pdf:
        raise HTTPException(status_code=409, detail="El reporte aun no esta listo.")
    contenido = _storage().read(reporte.ruta_pdf)
    return Response(
        content=contenido,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="reporte-{reporte.id}.pdf"'},
    )


def _contar_zonas_muertas(matriz: list[list[float]]) -> int:
    return sum(1 for fila in matriz for valor in fila if valor < -90)


def _reporte_out(reporte: Reporte) -> ReporteOut:
    return ReporteOut(
        id=reporte.id,
        proyecto_id=reporte.proyecto_id,
        escenario_id=reporte.escenario_id,
        estado=reporte.estado,
        url_descarga=_firmar_descarga(reporte.ruta_pdf) if reporte.ruta_pdf else None,
        sha256=reporte.sha256,
        tamanio_bytes=reporte.tamanio_bytes,
        error=reporte.error,
        created_at=reporte.created_at,
        updated_at=reporte.updated_at,
    )
