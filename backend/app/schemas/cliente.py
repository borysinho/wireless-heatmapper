"""Schemas Pydantic para la entidad Cliente.

Sprint 1 — PB-19: catálogo de clientes gestionado por el administrador.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class ClienteCreate(BaseModel):
    """Payload de entrada para crear un cliente. PB-19 — CA-1."""

    nombre: str
    email_referencia: EmailStr | None = None

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El nombre del cliente no puede estar vacío")
        return v

    @field_validator("email_referencia", mode="before")
    @classmethod
    def email_vacio_a_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = str(v).strip()
        return v or None


class ClienteUpdate(BaseModel):
    """Payload de entrada para actualizar un cliente. PB-19."""

    nombre: str | None = None
    email_referencia: EmailStr | None = None
    activo: bool | None = None

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("El nombre del cliente no puede estar vacío")
        return v

    @field_validator("email_referencia", mode="before")
    @classmethod
    def email_vacio_a_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = str(v).strip()
        return v or None


class ClienteBasicoOut(BaseModel):
    """DTO mínimo para incrustar en la respuesta de Proyecto."""

    id: int
    nombre: str
    email_referencia: str | None = None

    model_config = {"from_attributes": True}


class ClienteOut(BaseModel):
    """DTO completo para el listado de clientes del admin. PB-19."""

    id: int
    nombre: str
    email_referencia: str | None = None
    activo: bool
    created_at: datetime

    model_config = {"from_attributes": True}
