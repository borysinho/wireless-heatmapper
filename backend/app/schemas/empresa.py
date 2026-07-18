"""DTOs del sitio empresarial público."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ChatbotEmpresaPreguntaIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pregunta: str = Field(..., min_length=3, max_length=700)


class ChatbotEmpresaRespuestaOut(BaseModel):
    respuesta: str
    origen: Literal["azure_openai"]
