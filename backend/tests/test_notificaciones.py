"""Pruebas del registro FCM y de la notificación al asignar proyectos."""

from app.api.v1.admin_proyectos import get_notificacion_push_service
from app.main import app
from app.models.dispositivo_push import DispositivoPush


class NotificadorFalso:
    def __init__(self) -> None:
        self.asignaciones: list[dict] = []

    def notificar_asignacion(self, **datos) -> bool:
        self.asignaciones.append(datos)
        return True


def test_tecnico_registra_y_desregistra_dispositivo(
    client,
    tecnico_token,
    tecnico_usuario,
    db_session,
):
    token = "token-fcm-prueba-abcdefghijklmnopqrstuvwxyz"
    headers = {"Authorization": f"Bearer {tecnico_token}"}

    alta = client.post(
        "/notificaciones/dispositivos",
        headers=headers,
        json={"token": token, "plataforma": "android"},
    )
    assert alta.status_code == 201
    dispositivo = db_session.query(DispositivoPush).filter_by(token=token).one()
    assert dispositivo.usuario_id == tecnico_usuario.id
    assert dispositivo.activo is True

    baja = client.delete(
        "/notificaciones/dispositivos",
        headers=headers,
        json={"token": token, "plataforma": "android"},
    )
    assert baja.status_code == 204
    # La API usa otra sesión; cerrar la transacción de lectura de esta fixture
    # evita conservar la instantánea anterior en SQLite.
    db_session.rollback()
    db_session.refresh(dispositivo)
    assert dispositivo.activo is False


def test_admin_diagnostica_notificaciones_de_tecnico(
    client,
    admin_token,
    tecnico_usuario,
    db_session,
):
    db_session.add(
        DispositivoPush(
            usuario_id=tecnico_usuario.id,
            token="token-fcm-diagnostico-abcdefghijklmnopqrstuvwxyz",
            plataforma="android",
            activo=True,
        )
    )
    db_session.commit()

    respuesta = client.get(
        f"/notificaciones/diagnostico/{tecnico_usuario.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert respuesta.status_code == 200
    data = respuesta.json()
    assert data["usuario_id"] == tecnico_usuario.id
    assert data["tokens_activos"] == 1
    assert data["tokens_inactivos"] == 0
    assert data["ultimo_registro"] is not None
    assert "firebase_admin_configurado" in data


def test_tecnico_no_puede_ver_diagnostico_notificaciones(
    client,
    tecnico_token,
    tecnico_usuario,
):
    respuesta = client.get(
        f"/notificaciones/diagnostico/{tecnico_usuario.id}",
        headers={"Authorization": f"Bearer {tecnico_token}"},
    )

    assert respuesta.status_code == 403


def test_admin_crea_proyecto_y_notifica_al_tecnico(
    client,
    admin_token,
    tecnico_usuario,
):
    falso = NotificadorFalso()
    app.dependency_overrides[get_notificacion_push_service] = lambda: falso
    try:
        respuesta = client.post(
            "/admin/proyectos",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "nombre": "Survey Edificio Central",
                "descripcion": "Asignación desde el panel web",
                "cliente_id": None,
                "tecnico_id": tecnico_usuario.id,
                "estado": "nuevo",
            },
        )
    finally:
        app.dependency_overrides.pop(get_notificacion_push_service, None)

    assert respuesta.status_code == 201
    assert respuesta.json()["tecnico"]["id"] == tecnico_usuario.id
    assert falso.asignaciones[0]["tecnico_id"] == tecnico_usuario.id
    assert falso.asignaciones[0]["proyecto_nombre"] == "Survey Edificio Central"


def test_admin_edita_y_elimina_proyecto(
    client,
    admin_token,
    tecnico_usuario,
):
    falso = NotificadorFalso()
    app.dependency_overrides[get_notificacion_push_service] = lambda: falso
    headers = {"Authorization": f"Bearer {admin_token}"}
    try:
        alta = client.post(
            "/admin/proyectos",
            headers=headers,
            json={"nombre": "Temporal", "tecnico_id": tecnico_usuario.id},
        )
        proyecto_id = alta.json()["id"]
        edicion = client.put(
            f"/admin/proyectos/{proyecto_id}",
            headers=headers,
            json={"nombre": "Proyecto definitivo", "estado": "en_progreso"},
        )
        baja = client.delete(f"/admin/proyectos/{proyecto_id}", headers=headers)
    finally:
        app.dependency_overrides.pop(get_notificacion_push_service, None)

    assert edicion.status_code == 200
    assert edicion.json()["nombre"] == "Proyecto definitivo"
    assert edicion.json()["estado"] == "en_progreso"
    assert baja.status_code == 204
