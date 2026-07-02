"""DTOs para generación de conjuntos AP recomendados por IA."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.heatmap import (
    AlgoritmoHeatmap,
    ConjuntoAPOut,
    MapaCalorResumenOut,
)


class FuenteEntradaIAIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo: Literal["CONJUNTO_EXISTENTE"] = "CONJUNTO_EXISTENTE"
    conjunto_id: int = Field(..., gt=0)


class RestriccionesIAIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plano_id: int | None = Field(default=None, gt=0)
    fuente_entrada: FuenteEntradaIAIn
    umbral_objetivo_dbm: int = Field(default=-70, ge=-90, le=-50)
    algoritmo: AlgoritmoHeatmap = "IDW"
    resolucion: int = Field(default=64, ge=32, le=128)
    cantidad_aps_propuestos: int = Field(default=3, ge=1, le=8)
    cantidad_recomendaciones: int = Field(default=2, ge=1, le=5)


class ConjuntosIAGeneradosOut(BaseModel):
    conjunto_base_id: int
    mapa_actual: MapaCalorResumenOut
    conjuntos: list[ConjuntoAPOut]
    mapas_proyectados: list[MapaCalorResumenOut]


class PreparacionIAOut(BaseModel):
    plano_id: int
    conjunto_id: int
    mapa_actual_id: int
    cantidad_puntos: int
    preparado: bool = True
