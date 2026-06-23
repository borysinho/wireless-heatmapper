"""Pruebas del servicio de correo transaccional."""

from datetime import datetime

from app.services.email_service import EmailService


def test_invitacion_cliente_incluye_html_corporativo(monkeypatch):
    capturado: dict[str, str] = {}

    def fake_enviar(self, **kwargs):
        capturado.update(kwargs)
        return True

    monkeypatch.setattr(EmailService, "enviar", fake_enviar)

    enviado = EmailService().enviar_enlace_cliente(
        destinatario="cliente@test.bo",
        cliente="ACME & Hijos",
        nombre_proyecto="Sucursal <Norte>",
        url_publica="https://heatmapper.test/portal/token?x=1&y=2",
        expira_en=datetime(2026, 7, 6, 18, 30),
    )

    assert enviado is True
    assert capturado["destinatario"] == "cliente@test.bo"
    assert "Proyecto: Sucursal <Norte>" in capturado["cuerpo"]
    assert "Ver resultados" in capturado["html"]
    assert "Bulldog Tech." in capturado["html"]
    assert "ACME &amp; Hijos" in capturado["html"]
    assert "Sucursal &lt;Norte&gt;" in capturado["html"]
    assert "https://heatmapper.test/portal/token?x=1&amp;y=2" in capturado["html"]
