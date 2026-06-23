from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class DispositivoPushIn(BaseModel):
    token: str = Field(..., min_length=20, max_length=512)
    plataforma: Literal["android"] = "android"


class DispositivoPushOut(BaseModel):
    registrado: bool


class DiagnosticoNotificacionesOut(BaseModel):
    usuario_id: int
    tokens_activos: int
    tokens_inactivos: int
    ultimo_registro: datetime | None
    firebase_project_id_configurado: bool
    firebase_credentials_path_configurado: bool
    firebase_credentials_path_existe: bool
    firebase_credentials_json_configurado: bool
    google_application_credentials_configurado: bool
    google_application_credentials_existe: bool
    firebase_admin_configurado: bool
