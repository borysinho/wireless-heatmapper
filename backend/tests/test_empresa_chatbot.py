"""Tests del chatbot público del sitio empresarial."""

from app.api.v1.empresa import get_chatbot_empresa_service
from app.main import app
from app.services.chatbot_empresa_service import ChatbotEmpresaConfigError


class ChatbotEmpresaFalso:
    def __init__(self, respuesta: str = "Respuesta IA de prueba.") -> None:
        self.respuesta = respuesta
        self.preguntas: list[str] = []

    def responder(self, pregunta: str) -> str:
        self.preguntas.append(pregunta)
        return self.respuesta


class ChatbotEmpresaSinConfig:
    def responder(self, pregunta: str) -> str:
        raise ChatbotEmpresaConfigError("Falta configuración.")


def test_chatbot_empresa_responde_desde_servicio_ia(client):
    servicio = ChatbotEmpresaFalso("Team 24 Software desarrolla Wireless HeatMapper.")
    app.dependency_overrides[get_chatbot_empresa_service] = lambda: servicio

    respuesta = client.post(
        "/empresa/chatbot",
        json={"pregunta": "¿Qué es Wireless HeatMapper?"},
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "respuesta": "Team 24 Software desarrolla Wireless HeatMapper.",
        "origen": "azure_openai",
    }
    assert servicio.preguntas == ["¿Qué es Wireless HeatMapper?"]


def test_chatbot_empresa_valida_pregunta(client):
    respuesta = client.post("/empresa/chatbot", json={"pregunta": "no"})

    assert respuesta.status_code == 422


def test_chatbot_empresa_sin_configuracion_retorna_503(client):
    app.dependency_overrides[get_chatbot_empresa_service] = (
        lambda: ChatbotEmpresaSinConfig()
    )

    respuesta = client.post(
        "/empresa/chatbot",
        json={"pregunta": "¿Cómo contacto al equipo?"},
    )

    assert respuesta.status_code == 503
    assert respuesta.json()["detail"] == "El chatbot con IA no está configurado."
