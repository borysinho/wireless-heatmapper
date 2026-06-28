"""DTOs para generación de conjuntos AP recomendados por IA."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.heatmap import ConjuntoAPOut, MapaCalorOut

BandaWifi = Literal["2.4", "5"]


class FuenteEntradaIAIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo: Literal["CONJUNTO_EXISTENTE"] = "CONJUNTO_EXISTENTE"
    conjunto_id: int = Field(..., gt=0)


class RestriccionesIAIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plano_id: int | None = Field(default=None, gt=0)
    fuente_entrada: FuenteEntradaIAIn
    bandas: list[BandaWifi] = Field(default_factory=lambda: ["2.4", "5"], min_length=1)
    umbral_objetivo_dbm: int = Field(default=-70, ge=-90, le=-50)
    resolucion: int = Field(default=64, ge=32, le=128)
    cantidad_recomendaciones: int = Field(default=3, ge=1, le=5)

    @field_validator("bandas")
    @classmethod
    def normalizar_bandas(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(value))


class ConjuntosIAGeneradosOut(BaseModel):
    conjunto_base_id: int
    mapa_actual: MapaCalorOut
    conjuntos: list[ConjuntoAPOut]
    mapas_proyectados: list[MapaCalorOut]
