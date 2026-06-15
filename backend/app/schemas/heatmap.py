"""DTOs del módulo de heatmap y análisis.

Sprint 4 — PB-05, PB-06.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

AlgoritmoHeatmap = Literal["IDW", "KRIGING"]
ResolucionHeatmap = Literal[64, 128, 256]


class EscalaHeatmapItem(BaseModel):
    desde: int
    hasta: int
    color: str
    etiqueta: str


class PuntoLecturaHeatmapOut(BaseModel):
    punto_id: int
    pos_x: float
    pos_y: float
    rssi: float


class MapaCalorOut(BaseModel):
    id: int
    plano_id: int
    algoritmo: str
    resolucion: int
    bssid: str
    ssid: str
    ap_pos_x: float
    ap_pos_y: float
    aps_interes: list[APDisponibleOut]
    url_imagen: str
    matriz: list[list[float]]
    escala: list[EscalaHeatmapItem]
    cantidad_puntos: int
    rssi_min: float
    rssi_max: float
    rssi_promedio: float
    puntos_lectura: list[PuntoLecturaHeatmapOut]
    advertencias: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class APDetectadoOut(BaseModel):
    id: int
    bssid: str
    ssid: str
    canal: int | None
    frecuencia_mhz: int | None
    rssi_promedio: float
    pos_x: float
    pos_y: float
    confirmado: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class APDisponibleOut(BaseModel):
    bssid: str
    ssid: str
    canal: int | None
    frecuencia_mhz: int | None
    rssi_promedio: float
    pos_x: float
    pos_y: float
    cantidad_puntos: int


class AnalisisCoberturaOut(BaseModel):
    id: int
    mapa_calor_id: int
    pct_cobertura: float
    pct_zonas_muertas: float
    celdas_zonas_muertas: int
    cantidad_solapamientos: int
    cantidad_interferencias: int
    hallazgos: dict
    resumen: str
    aps_detectados: list[APDetectadoOut]
    created_at: datetime

    model_config = {"from_attributes": True}


class ConfirmarAPIn(BaseModel):
    pos_x: float = Field(..., ge=0)
    pos_y: float = Field(..., ge=0)
    confirmado: bool = True
