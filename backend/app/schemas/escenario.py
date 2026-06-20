"""DTOs de Sprint 5: escenarios IA, comparación y reportes."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.heatmap import MapaCalorOut

BandaWifi = Literal["2.4", "5"]
AccionRecomendacion = Literal[
    "MANTENER", "AGREGAR", "MOVER", "RECONFIGURAR", "CAMBIAR_MODELO", "RETIRAR"
]


class RestriccionesEscenarioIn(BaseModel):
    max_aps: int = Field(default=3, ge=1, le=5)
    presupuesto: float | None = Field(default=None, gt=0)
    banda_preferida: BandaWifi = "5"
    bandas: list[BandaWifi] = Field(default_factory=lambda: ["2.4", "5"], min_length=1)
    tipo_negocio: Literal["INSTALACION_NUEVA", "RED_EXISTENTE"] = "INSTALACION_NUEVA"
    perfil: Literal[
        "COBERTURA_EQUILIBRADA", "PRIORIZAR_5_GHZ", "MENOR_COSTO_CAMBIOS"
    ] = "COBERTURA_EQUILIBRADA"
    politica_combinacion: Literal[
        "MEJOR_BANDA_COMPATIBLE", "PREFERIR_5_GHZ_SI_CUMPLE_UMBRAL", "SOLO_DUAL_BAND"
    ] = "PREFERIR_5_GHZ_SI_CUMPLE_UMBRAL"
    modelo_ap: str = Field(
        default="AP WiFi 6 Bulldog BT-AX1800", min_length=3, max_length=120
    )
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
    altura_m: float
    tipo_montaje: str
    banda: str
    modelo_ap: str
    costo_estimado: float
    rssi_proyectado: float
    radios: list[dict]
    justificacion: str

    model_config = {"from_attributes": True}


class EscenarioOptimizadoOut(BaseModel):
    id: int
    proyecto_id: int
    plano_id: int
    mapa_actual_id: int | None
    mapa_proyectado_id: int | None
    nombre: str
    tipo_negocio: str
    perfil: str
    politica_combinacion: str
    banda: str
    bandas: list[str]
    modelo_ap: str
    pct_cobertura_actual: float
    pct_cobertura: float
    costo_estimado: float
    cantidad_aps: int
    resumen: str
    restricciones: dict
    metricas: dict
    mapas_por_banda: dict
    mapas_actuales_por_banda: dict
    supuestos: list[str]
    confianza: str
    version_motor: str
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
    comparacion_por_banda: dict = Field(default_factory=dict)
    resumen: ResumenComparacionOut


class ValorProyectadoPuntoOut(BaseModel):
    id: int
    escenario_id: int
    punto_medicion_id: int
    banda: str
    rssi_observado_dbm: float | None
    rssi_proyectado_dbm: float
    diferencia_db: float | None
    radio_primaria: str
    radio_secundaria: str | None
    rssi_secundario_dbm: float | None
    snr_proyectado_db: float | None
    incertidumbre_db: float

    model_config = {"from_attributes": True}


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
