"""Servicio SMTP para correos transaccionales."""

# ruff: noqa: E501

from __future__ import annotations

import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage
from html import escape

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
        fecha_expiracion = f"{expira_en:%Y-%m-%d %H:%M}"
        cuerpo = "\n".join(
            [
                saludo,
                "",
                "Bulldog Tech. compartió contigo los resultados publicados "
                "del relevamiento WiFi.",
                "",
                f"Proyecto: {nombre_proyecto}",
                f"Enlace: {url_publica}",
                f"Vigente hasta: {fecha_expiracion}",
                "",
                "El enlace muestra únicamente el contenido autorizado para cliente.",
                "",
                "Wireless HeatMapper",
            ]
        )
        html = _plantilla_enlace_cliente_html(
            cliente=cliente,
            nombre_proyecto=nombre_proyecto,
            url_publica=url_publica,
            fecha_expiracion=fecha_expiracion,
        )
        return self.enviar(
            destinatario=destinatario,
            asunto=asunto,
            cuerpo=cuerpo,
            html=html,
        )

    def enviar(
        self,
        *,
        destinatario: str,
        asunto: str,
        cuerpo: str,
        html: str | None = None,
    ) -> bool:
        if not self.habilitado:
            logger.info("Correo transaccional omitido: SMTP no habilitado.")
            return False

        remitente = self._settings.smtp_from_email or self._settings.smtp_username
        mensaje = EmailMessage()
        mensaje["From"] = f"{self._settings.smtp_from_name} <{remitente}>"
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.set_content(cuerpo)
        if html is not None:
            mensaje.add_alternative(html, subtype="html")

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


def _plantilla_enlace_cliente_html(
    *,
    cliente: str | None,
    nombre_proyecto: str,
    url_publica: str,
    fecha_expiracion: str,
) -> str:
    saludo = f"Hola {escape(cliente)}," if cliente else "Hola,"
    proyecto = escape(nombre_proyecto)
    url = escape(url_publica, quote=True)
    expiracion = escape(fecha_expiracion)
    return f"""\
<!doctype html>
<html lang="es">
  <body style="margin:0;padding:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#172033;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f4f7fb;padding:28px 12px;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:620px;background:#ffffff;border:1px solid #d8e2ef;border-radius:8px;overflow:hidden;">
            <tr>
              <td style="background:#0f3d5e;padding:22px 28px;color:#ffffff;">
                <div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#b9d7ea;">Bulldog Tech.</div>
                <h1 style="margin:8px 0 0;font-size:22px;line-height:1.25;font-weight:700;">Resultados WiFi disponibles</h1>
              </td>
            </tr>
            <tr>
              <td style="padding:28px;">
                <p style="margin:0 0 16px;font-size:16px;line-height:1.5;">{saludo}</p>
                <p style="margin:0 0 20px;font-size:15px;line-height:1.6;color:#3a4658;">
                  Bulldog Tech. compartió contigo los resultados publicados del relevamiento WiFi.
                </p>
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin:0 0 22px;border:1px solid #e2e8f0;border-radius:8px;background:#f8fafc;">
                  <tr>
                    <td style="padding:16px 18px;">
                      <div style="font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#64748b;">Proyecto</div>
                      <div style="margin-top:4px;font-size:17px;font-weight:700;color:#172033;">{proyecto}</div>
                      <div style="margin-top:12px;font-size:13px;color:#64748b;">Vigente hasta: <strong style="color:#172033;">{expiracion}</strong></div>
                    </td>
                  </tr>
                </table>
                <p style="margin:0 0 24px;text-align:center;">
                  <a href="{url}" style="display:inline-block;background:#1f6f9f;color:#ffffff;text-decoration:none;font-size:15px;font-weight:700;padding:12px 22px;border-radius:6px;">Ver resultados</a>
                </p>
                <p style="margin:0 0 10px;font-size:13px;line-height:1.5;color:#64748b;">
                  Si el botón no abre, copia y pega este enlace en tu navegador:
                </p>
                <p style="margin:0;font-size:13px;line-height:1.5;word-break:break-all;color:#1f6f9f;">{url}</p>
              </td>
            </tr>
            <tr>
              <td style="padding:16px 28px;background:#f8fafc;border-top:1px solid #e2e8f0;color:#64748b;font-size:12px;line-height:1.5;">
                El enlace muestra únicamente el contenido autorizado para cliente. Wireless HeatMapper.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
