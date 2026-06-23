"""Registro de dispositivos del técnico para recibir notificaciones FCM."""

import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.models.usuario import Usuario
from app.repositories.dispositivo_push_repository import DispositivoPushRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.notificacion import (
    DiagnosticoNotificacionesOut,
    DispositivoPushIn,
    DispositivoPushOut,
)

router = APIRouter(prefix="/notificaciones", tags=["notificaciones"])


@router.post(
    "/dispositivos",
    response_model=DispositivoPushOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar dispositivo para notificaciones",
)
def registrar_dispositivo(
    body: DispositivoPushIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> DispositivoPushOut:
    DispositivoPushRepository(db).registrar(
        usuario_id=current_user.id,
        token=body.token,
        plataforma=body.plataforma,
    )
    return DispositivoPushOut(registrado=True)


@router.delete(
    "/dispositivos",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desregistrar dispositivo",
)
def desregistrar_dispositivo(
    body: DispositivoPushIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    DispositivoPushRepository(db).desactivar(
        usuario_id=current_user.id,
        token=body.token,
    )


@router.get(
    "/diagnostico/{usuario_id}",
    response_model=DiagnosticoNotificacionesOut,
    summary="Diagnosticar notificaciones de un usuario",
)
def diagnosticar_notificaciones(
    usuario_id: int,
    db: Session = Depends(get_db),
    _admin: Usuario = Depends(require_admin),
) -> DiagnosticoNotificacionesOut:
    usuario = UsuarioRepository(db).obtener_por_id(usuario_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    tokens_activos, tokens_inactivos, ultimo_registro = (
        DispositivoPushRepository(db).resumir_usuario(usuario_id=usuario_id)
    )
    ruta_credenciales = (
        Path(settings.firebase_credentials_path)
        if settings.firebase_credentials_path
        else None
    )
    ruta_adc = (
        Path(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        else None
    )
    credentials_path_existe = bool(ruta_credenciales and ruta_credenciales.is_file())
    google_credentials_existe = bool(ruta_adc and ruta_adc.is_file())
    credentials_json_configurado = bool(settings.firebase_credentials_json)

    return DiagnosticoNotificacionesOut(
        usuario_id=usuario_id,
        tokens_activos=tokens_activos,
        tokens_inactivos=tokens_inactivos,
        ultimo_registro=ultimo_registro,
        firebase_project_id_configurado=bool(settings.firebase_project_id),
        firebase_credentials_path_configurado=ruta_credenciales is not None,
        firebase_credentials_path_existe=credentials_path_existe,
        firebase_credentials_json_configurado=credentials_json_configurado,
        google_application_credentials_configurado=ruta_adc is not None,
        google_application_credentials_existe=google_credentials_existe,
        firebase_admin_configurado=(
            credentials_json_configurado
            or credentials_path_existe
            or google_credentials_existe
        ),
    )
