"""Servicio SMTP para correos transaccionales."""

from __future__ import annotations

import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage

from app.core.config import Settings, settings
from app.models.usuario import Usuario

logger = logging.getLogger(__name__)


class EmailDeliveryError(RuntimeError):
    """Error controlado cuando el servidor SMTP rechaza un correo."""


class EmailService:
    def __init__(self, configuracion: Settings = settings) -> None:
        self._settings = configuracion

    @property
    def habilitado(self) -> bool:
        return bool(
            self._settings.email_notifications_enabled
            and self._settings.smtp_host
            and self._settings.smtp_username
            and self._settings.smtp_password
        )

    def enviar_cuenta_creada(
        self,
        *,
        usuario: Usuario,
        password_temporal: str,
    ) -> bool:
        asunto = "Tu cuenta de Wireless HeatMapper fue creada"
        cuerpo = "\n".join(
            [
                f"Hola {usuario.nombre},",
                "",
                "Se creó tu cuenta para acceder a Wireless HeatMapper.",
                "",
                f"Correo: {usuario.email}",
                f"Contraseña temporal: {password_temporal}",
                f"Rol: {usuario.rol}",
                "",
                "Por seguridad, cambia esta contraseña después del primer ingreso.",
                "",
                "Bulldog Tech.",
            ]
        )
        return self.enviar(destinatario=usuario.email, asunto=asunto, cuerpo=cuerpo)

    def enviar_enlace_cliente(
        self,
        *,
        destinatario: str,
        nombre_proyecto: str,
        url_publica: str,
        expira_en: datetime,
        cliente: str | None = None,
    ) -> bool:
        asunto = f"Resultados WiFi disponibles: {nombre_proyecto}"
        saludo = f"Hola {cliente}," if cliente else "Hola,"
        cuerpo = "\n".join(
            [
                saludo,
                "",
                "Bulldog Tech. compartió contigo los resultados publicados "
                "del relevamiento WiFi.",
                "",
                f"Proyecto: {nombre_proyecto}",
                f"Enlace: {url_publica}",
                f"Vigente hasta: {expira_en:%Y-%m-%d %H:%M}",
                "",
                "El enlace muestra únicamente el contenido autorizado para cliente.",
                "",
                "Wireless HeatMapper",
            ]
        )
        return self.enviar(destinatario=destinatario, asunto=asunto, cuerpo=cuerpo)

    def enviar(self, *, destinatario: str, asunto: str, cuerpo: str) -> bool:
        if not self.habilitado:
            logger.info("Correo transaccional omitido: SMTP no habilitado.")
            return False

        remitente = self._settings.smtp_from_email or self._settings.smtp_username
        mensaje = EmailMessage()
        mensaje["From"] = f"{self._settings.smtp_from_name} <{remitente}>"
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.set_content(cuerpo)

        try:
            with smtplib.SMTP(
                self._settings.smtp_host,
                self._settings.smtp_port,
                timeout=self._settings.smtp_timeout_seconds,
            ) as smtp:
                if self._settings.smtp_use_tls:
                    smtp.starttls()
                smtp.login(
                    self._settings.smtp_username,
                    self._settings.smtp_password,
                )
                smtp.send_message(mensaje)
        except (OSError, smtplib.SMTPException) as exc:
            logger.exception("No se pudo enviar correo transaccional.")
            raise EmailDeliveryError("No se pudo enviar el correo.") from exc

        return True
