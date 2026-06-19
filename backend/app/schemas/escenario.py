"""DTOs de Sprint 5: escenarios IA, comparación y reportes."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.heatmap import MapaCalorOut

BandaWifi = Literal["2.4", "5", "6"]
AccionRecomendacion = Literal["AGREGAR", "MOVER", "CAMBIAR_MODELO", "REMOVER"]


class RestriccionesEscenarioIn(BaseModel):
    max_aps: int = Field(default=3, ge=1, le=5)
    presupuesto: float | None = Field(default=None, gt=0)
    banda_preferida: BandaWifi = "5"
    modelo_ap: str = Field(default="AP WiFi 6 Bulldog BT-AX1800", min_length=3, max_length=120)
    costo_unitario: float = Field(default=120.0, gt=0)
    resolucion: int = Field(default=64, ge=32, le=128)

    @field_validator("modelo_ap")
    @classmethod
    def limpiar_modelo(cls, value: str) -> str:
        return value.strip()


class RecomendacionAPOut(BaseModel):
    id: int
    orden: int
    accion: str
    coord_x: float
    coord_y: float
    banda: str
    modelo_ap: str
    costo_estimado: float
    rssi_proyectado: float
    justificacion: str

    model_config = {"from_attributes": True}


class EscenarioOptimizadoOut(BaseModel):
    id: int
    proyecto_id: int
    plano_id: int
    mapa_actual_id: int | None
    mapa_proyectado_id: int | None
    nombre: str
    banda: str
    modelo_ap: str
    pct_cobertura_actual: float
    pct_cobertura: float
    costo_estimado: float
    cantidad_aps: int
    resumen: str
    restricciones: dict
    metricas: dict
    recomendaciones: list[RecomendacionAPOut]
    created_at: datetime

    model_config = {"from_attributes": True}


class EscenariosGeneradosOut(BaseModel):
    escenarios: list[EscenarioOptimizadoOut]


class ResumenComparacionOut(BaseModel):
    delta_pct_cobertura: float
    delta_zonas_muertas: int
    costo_estimado: float
    cantidad_cambios: int
    lectura: str


class ComparacionEscenarioOut(BaseModel):
    escenario: EscenarioOptimizadoOut
    heatmap_actual: MapaCalorOut
    heatmap_proyectado: MapaCalorOut
    matriz_diferencia: list[list[float]]
    resumen: ResumenComparacionOut


class ReporteCrearIn(BaseModel):
    escenario_id: int | None = None
    incluir_csv: bool = False


class ReporteOut(BaseModel):
    id: int
    proyecto_id: int
    escenario_id: int | None
    estado: str
    url_descarga: str | None
    sha256: str | None
    tamanio_bytes: int
    error: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
