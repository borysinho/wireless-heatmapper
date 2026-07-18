"""Servicio del chatbot público empresarial con Azure OpenAI."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from app.core.config import settings


class ChatbotEmpresaConfigError(RuntimeError):
    """La integración de Azure OpenAI no está configurada."""


class ChatbotEmpresaGenerationError(RuntimeError):
    """El modelo no pudo generar una respuesta utilizable."""


class ChatbotEmpresaService:
    """Responde consultas públicas con información aprobada del proyecto."""

    api_version = "2025-04-01-preview"

    def responder(self, pregunta: str) -> str:
        self._validar_configuracion()
        data = self._post_responses(self._payload(pregunta.strip()))
        respuesta = self._extraer_texto(data)
        if not respuesta:
            raise ChatbotEmpresaGenerationError("El modelo no devolvió texto.")
        return respuesta[:1400]

    def _validar_configuracion(self) -> None:
        if not settings.azure_openai_api_key.strip():
            raise ChatbotEmpresaConfigError("Falta AZURE_OPENAI_API_KEY.")
        if not settings.azure_openai_endpoint.strip():
            raise ChatbotEmpresaConfigError("Falta AZURE_OPENAI_ENDPOINT.")
        if not self._deployment().strip():
            raise ChatbotEmpresaConfigError(
                "Falta AZURE_OPENAI_CHATBOT_DEPLOYMENT."
            )

    def _deployment(self) -> str:
        return (
            settings.azure_openai_chatbot_deployment.strip()
            or settings.azure_openai_poligono_deployment.strip()
        )

    def _payload(self, pregunta: str) -> dict[str, Any]:
        contexto = (
            "Eres el asistente público de Team 24 Software para el sitio "
            "empresarial del proyecto académico Wireless HeatMapper. Responde "
            "siempre en español de Bolivia, con tono profesional y conciso. "
            "Usa solo información aprobada: Team 24 Software es el equipo "
            "desarrollador del Grupo 24 de Ingeniería de Software II, Santa "
            "Cruz de la Sierra; Bulldog Tech. es el cliente del caso de "
            "estudio. El producto integra portal web React, backend FastAPI, "
            "PostgreSQL, app Android Flutter, mapas de calor WiFi e IA backend. "
            "La modalidad oficial es 100 % en línea, sin base local de dominio "
            "ni sincronización diferida. El objetivo técnico de diseño visible "
            "es RSSI >= -70 dBm y RSSI < -90 dBm se interpreta como zona muerta. "
            "El panel administrativo está en /admin/login, el manual en /manual/ "
            "y la API técnica en /api/docs. El contacto autorizado es "
            "borysquiroga@gmail.com, teléfono +591-77685777 y WhatsApp "
            "+591-77685777. No pidas contraseñas, tokens, claves WiFi reales ni "
            "secretos de infraestructura. No inventes precios, contratos, "
            "fechas de release ni compromisos comerciales; si falta un dato, "
            "deriva al correo de contacto."
        )
        return {
            "model": self._deployment(),
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": contexto}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": pregunta}],
                },
            ],
            "max_output_tokens": 450,
            "reasoning": {"effort": "minimal"},
        }

    def _post_responses(self, payload: dict[str, Any]) -> dict[str, Any]:
        endpoint = settings.azure_openai_endpoint.rstrip("/")
        url = f"{endpoint}/openai/responses?api-version={self.api_version}"
        request = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "api-key": settings.azure_openai_api_key,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=settings.azure_openai_chatbot_timeout_seconds,
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detalle = exc.read().decode("utf-8", errors="ignore")
            raise ChatbotEmpresaGenerationError(
                f"Azure OpenAI rechazó la solicitud: {detalle[:300]}"
            ) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ChatbotEmpresaGenerationError(
                "No se pudo conectar con Azure OpenAI."
            ) from exc

    def _extraer_texto(self, data: dict[str, Any]) -> str:
        textos: list[str] = []
        for salida in data.get("output", []):
            for contenido in salida.get("content", []):
                if contenido.get("type") == "output_text":
                    textos.append(str(contenido.get("text", "")))
        return "\n".join(texto for texto in textos if texto.strip()).strip()
