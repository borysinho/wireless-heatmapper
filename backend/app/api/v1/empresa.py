"""Endpoints públicos del sitio empresarial."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.empresa import (
    ChatbotEmpresaPreguntaIn,
    ChatbotEmpresaRespuestaOut,
)
from app.services.chatbot_empresa_service import (
    ChatbotEmpresaConfigError,
    ChatbotEmpresaGenerationError,
    ChatbotEmpresaService,
)

router = APIRouter(prefix="/empresa", tags=["sitio-empresa"])


def get_chatbot_empresa_service() -> ChatbotEmpresaService:
    return ChatbotEmpresaService()


@router.post(
    "/chatbot",
    response_model=ChatbotEmpresaRespuestaOut,
    summary="Consultar chatbot empresarial",
    description=(
        "Responde consultas públicas del sitio empresarial mediante Azure OpenAI "
        "sin exponer credenciales al frontend."
    ),
)
def consultar_chatbot_empresa(
    body: ChatbotEmpresaPreguntaIn,
    service: ChatbotEmpresaService = Depends(get_chatbot_empresa_service),
) -> ChatbotEmpresaRespuestaOut:
    try:
        respuesta = service.responder(body.pregunta)
    except ChatbotEmpresaConfigError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El chatbot con IA no está configurado.",
        ) from exc
    except ChatbotEmpresaGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo obtener respuesta del asistente IA.",
        ) from exc

    return ChatbotEmpresaRespuestaOut(respuesta=respuesta, origen="azure_openai")
