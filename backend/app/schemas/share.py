"""DTOs del portal público de cliente.

Sprint 6 — PB-15/PB-16/PB-17.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.heatmap import ConjuntoAPOut, MapaCalorOut
from app.schemas.plano import PlanoOut


class ContenidoEnlaceIn(BaseModel):
    conjunto_ids: list[int] = Field(default_factory=list)
    mapa_ids: list[int] = Field(default_factory=list)


class EnlaceClienteCrearIn(BaseModel):
    expira_en_dias: int = Field(default=7, ge=1, le=365)
    contenido: ContenidoEnlaceIn
    cliente_id: int | None = None


class EnlaceClienteEnviarCorreoIn(BaseModel):
    cliente_id: int


class EnlaceClienteEnviarCorreoOut(BaseModel):
    enlace_id: int
    destinatario: str
    enviado: bool


class EnlaceClienteActualizarIn(BaseModel):
    revocado: bool


class EnlaceClienteOut(BaseModel):
    id: int
    proyecto_id: int
    url_publica: str
    expira_en: datetime
    revocado: bool
    accesos: int
    ultimo_acceso: datetime | None
    ip_ultimo_acceso: str | None
    contenido: ContenidoEnlaceIn
    created_at: datetime


class ProyectoPortalOut(BaseModel):
    id: int
    nombre: str
    cliente: str | None
    descripcion: str | None


class PortalClienteOut(BaseModel):
    proyecto: ProyectoPortalOut
    planos: list[PlanoOut]
    conjuntos: list[ConjuntoAPOut]
    heatmaps: list[MapaCalorOut]
