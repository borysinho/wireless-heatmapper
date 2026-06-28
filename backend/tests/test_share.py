"""Tests Sprint 6 — portal cliente en modalidad online."""

from datetime import UTC, datetime, timedelta

from app.core.config import settings
from app.models.cliente import Cliente
from app.models.heatmap import ConjuntoAP, ConjuntoAPItem, MapaCalor
from app.models.plano import Plano
from app.models.proyecto import Proyecto
from app.models.share import TokenEnlaceCliente
from app.repositories.medicion_repository import MedicionRepository
from app.schemas.medicion import MedicionItemIn
from app.services.email_service import EmailService


def _crear_proyecto_publicable(db, tecnico):
    proyecto = Proyecto(
        nombre="Portal Cliente Bulldog",
        descripcion="Resultado final para cliente.",
        tecnico_id=tecnico.id,
    )
    db.add(proyecto)
    db.flush()
    plano = Plano(
        proyecto_id=proyecto.id,
        nombre="planta.png",
        formato="png",
        ruta_storage=f"portal/{proyecto.id}/planta.png",
        ancho_px=400,
        alto_px=300,
        tamano_bytes=100,
        calibracion_x1=0,
        calibracion_y1=0,
        calibracion_x2=100,
        calibracion_y2=0,
        distancia_real_m=10,
        escala_m_por_px=0.1,
        poligono_interes=[
            {"x": 0, "y": 0},
            {"x": 400, "y": 0},
            {"x": 400, "y": 300},
            {"x": 0, "y": 300},
        ],
    )
    db.add(plano)
    db.flush()
    mapa = MapaCalor(
        plano_id=plano.id,
        modo_generacion="CONJUNTO_COMPLETO",
        algoritmo="IDW",
        resolucion=32,
        bssid="aa:bb:cc:dd:ee:01",
        ssid="BulldogCorp",
        ap_pos_x=100,
        ap_pos_y=120,
        aps_interes=[
            {
                "bssid": "aa:bb:cc:dd:ee:01",
                "ssid": "BulldogCorp",
                "canal": 6,
                "frecuencia_mhz": 2437,
                "rssi_promedio": -62,
                "pos_x": 100,
                "pos_y": 120,
                "cantidad_puntos": 5,
            }
        ],
        bssids_generacion=["aa:bb:cc:dd:ee:01"],
        matriz=[[-62.0 for _ in range(32)] for _ in range(32)],
        escala=[{"desde": -70, "hasta": -60, "color": "#2ecc71", "etiqueta": "Buena"}],
        ruta_imagen=f"heatmaps/{plano.id}/portal.png",
        cantidad_puntos=5,
        rssi_min=-70,
        rssi_max=-55,
        firma_mediciones="portal-test",
    )
    db.add(mapa)
    db.commit()
    db.refresh(proyecto)
    db.refresh(mapa)
    return proyecto, mapa


def _crear_conjunto_con_mediciones(db, proyecto):
    plano = proyecto.planos[0]
    repo = MedicionRepository(db)
    for x, y, rssi in [
        (20, 20, -45),
        (380, 20, -62),
        (20, 280, -74),
        (380, 280, -88),
        (200, 150, -92),
    ]:
        repo.crear_lote(
            plano_id=plano.id,
            pos_x=x,
            pos_y=y,
            items=[
                MedicionItemIn(
                    ssid="BulldogCorp",
                    bssid="aa:bb:cc:dd:ee:01",
                    rssi=rssi,
                    canal=6,
                    frecuencia_mhz=2437,
                )
            ],
        )
    conjunto = ConjuntoAP(
        plano_id=plano.id,
        nombre="Conjunto cliente",
        proposito="Cobertura cliente",
        origen="manual_web",
        creado_por_id=proyecto.tecnico_id,
    )
    db.add(conjunto)
    db.flush()
    db.add(
        ConjuntoAPItem(
            conjunto_ap_id=conjunto.id,
            bssid="aa:bb:cc:dd:ee:01",
            ssid_snapshot="BulldogCorp",
            canal_snapshot=6,
            rssi_promedio_snapshot=-72.2,
            pos_x=100,
            pos_y=120,
        )
    )
    db.commit()
    db.refresh(conjunto)
    return conjunto


def test_enlace_cliente_expone_solo_contenido_autorizado(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, mapa = _crear_proyecto_publicable(db_session, tecnico_usuario)

    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "expira_en_dias": 7,
            "contenido": {"mapa_ids": [mapa.id]},
        },
    )
    assert respuesta.status_code == 201
    enlace = respuesta.json()
    assert enlace["url_publica"].startswith("/portal/")
    assert enlace["contenido"]["mapa_ids"] == [mapa.id]

    token = enlace["url_publica"].removeprefix("/portal/")
    portal = client.get(f"/share/{token}")
    assert portal.status_code == 200
    payload = portal.json()
    assert payload["proyecto"]["nombre"] == "Portal Cliente Bulldog"
    assert [item["id"] for item in payload["heatmaps"]] == [mapa.id]
    assert payload["conjuntos"] == []

    db_session.expire_all()
    enlace_db = db_session.query(TokenEnlaceCliente).filter_by(id=enlace["id"]).one()
    assert enlace_db.accesos == 1
    assert enlace_db.ultimo_acceso is not None


def test_enlace_cliente_envia_correo_al_cliente_seleccionado(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
    monkeypatch,
):
    proyecto, mapa = _crear_proyecto_publicable(db_session, tecnico_usuario)
    cliente = Cliente(
        nombre="Cliente con correo",
        email_referencia="cliente@test.bo",
    )
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    envios: list[dict[str, str]] = []

    def fake_enviar_enlace_cliente(self, **kwargs):
        envios.append(kwargs)
        return True

    monkeypatch.setattr(
        EmailService,
        "enviar_enlace_cliente",
        fake_enviar_enlace_cliente,
    )
    monkeypatch.setattr(EmailService, "habilitado", property(lambda self: True))
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "expira_en_dias": 7,
            "cliente_id": cliente.id,
            "contenido": {"mapa_ids": [mapa.id]},
        },
    )

    assert respuesta.status_code == 201
    assert envios[0]["destinatario"] == "cliente@test.bo"
    assert envios[0]["cliente"] == "Cliente con correo"
    assert envios[0]["nombre_proyecto"] == "Portal Cliente Bulldog"
    assert envios[0]["url_publica"].startswith("http://testserver/portal/")


def test_enlace_cliente_no_crea_si_correo_no_esta_configurado(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
    monkeypatch,
):
    proyecto, mapa = _crear_proyecto_publicable(db_session, tecnico_usuario)
    cliente = Cliente(
        nombre="Cliente con correo",
        email_referencia="cliente@test.bo",
    )
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    monkeypatch.setattr(EmailService, "habilitado", property(lambda self: False))

    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "expira_en_dias": 7,
            "cliente_id": cliente.id,
            "contenido": {"mapa_ids": [mapa.id]},
        },
    )

    assert respuesta.status_code == 503
    assert respuesta.json()["detail"] == "El correo transaccional no está configurado."
    assert db_session.query(TokenEnlaceCliente).count() == 0


def test_enlace_generado_puede_enviarse_por_correo(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
    monkeypatch,
):
    proyecto, mapa = _crear_proyecto_publicable(db_session, tecnico_usuario)
    cliente = Cliente(
        nombre="Cliente destino",
        email_referencia="cliente@test.bo",
    )
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    envios: list[dict[str, str]] = []

    def fake_enviar_enlace_cliente(self, **kwargs):
        envios.append(kwargs)
        return True

    monkeypatch.setattr(
        EmailService,
        "enviar_enlace_cliente",
        fake_enviar_enlace_cliente,
    )
    monkeypatch.setattr(EmailService, "habilitado", property(lambda self: True))
    creado = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"expira_en_dias": 7, "contenido": {"mapa_ids": [mapa.id]}},
    )
    enlace = creado.json()

    respuesta = client.post(
        f"/share/enlaces/{enlace['id']}/correo",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"cliente_id": cliente.id},
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "enlace_id": enlace["id"],
        "destinatario": "cliente@test.bo",
        "enviado": True,
    }
    assert envios[0]["destinatario"] == "cliente@test.bo"
    assert envios[0]["cliente"] == "Cliente destino"


def test_enlace_generado_no_envia_correo_si_esta_revocado(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, mapa = _crear_proyecto_publicable(db_session, tecnico_usuario)
    cliente = Cliente(
        nombre="Cliente destino",
        email_referencia="cliente@test.bo",
    )
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    creado = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"expira_en_dias": 7, "contenido": {"mapa_ids": [mapa.id]}},
    )
    enlace = creado.json()
    client.patch(
        f"/share/enlaces/{enlace['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"revocado": True},
    )

    respuesta = client.post(
        f"/share/enlaces/{enlace['id']}/correo",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"cliente_id": cliente.id},
    )

    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == "No se puede enviar un enlace revocado."


def test_enlace_cliente_rechaza_cliente_sin_correo_referencia(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, mapa = _crear_proyecto_publicable(db_session, tecnico_usuario)
    cliente = Cliente(nombre="Cliente sin correo")
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)

    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "expira_en_dias": 7,
            "cliente_id": cliente.id,
            "contenido": {"mapa_ids": [mapa.id]},
        },
    )

    assert respuesta.status_code == 422
    assert (
        respuesta.json()["detail"]
        == "El cliente seleccionado no tiene correo de referencia registrado."
    )
    assert db_session.query(TokenEnlaceCliente).count() == 0


def test_enlace_cliente_revocado_o_expirado_devuelve_404(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, mapa = _crear_proyecto_publicable(db_session, tecnico_usuario)
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"expira_en_dias": 1, "contenido": {"mapa_ids": [mapa.id]}},
    )
    enlace = respuesta.json()
    token = enlace["url_publica"].removeprefix("/portal/")

    revocado = client.patch(
        f"/share/enlaces/{enlace['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"revocado": True},
    )
    assert revocado.status_code == 200
    assert client.get(f"/share/{token}").status_code == 404

    enlace_db = db_session.query(TokenEnlaceCliente).filter_by(id=enlace["id"]).one()
    enlace_db.revocado = False
    enlace_db.expira_en = datetime.now(UTC) - timedelta(minutes=1)
    db_session.commit()
    assert client.get(f"/share/{token}").status_code == 404


def test_portal_genera_heatmap_desde_conjunto_y_reutiliza_cache(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(settings, "storage_root", str(tmp_path))
    monkeypatch.setattr(
        settings,
        "storage_url_secret",
        "test_secret_32chars_minimo_xxxxxx",
    )
    proyecto, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
    conjunto = _crear_conjunto_con_mediciones(db_session, proyecto)
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"contenido": {"conjunto_ids": [conjunto.id]}},
    )
    assert respuesta.status_code == 201
    token = respuesta.json()["url_publica"].removeprefix("/portal/")

    body = {
        "modo": "CONJUNTO_COMPLETO",
        "algoritmo": "IDW",
        "resolucion": 64,
    }
    primera = client.post(
        f"/share/{token}/conjuntos/{conjunto.id}/heatmaps",
        json=body,
    )
    assert primera.status_code == 200
    mapa_1 = primera.json()
    assert mapa_1["conjunto_ap_id"] == conjunto.id
    assert mapa_1["modo_generacion"] == "CONJUNTO_COMPLETO"

    segunda = client.post(
        f"/share/{token}/conjuntos/{conjunto.id}/heatmaps",
        json=body,
    )
    assert segunda.status_code == 200
    assert segunda.json()["id"] == mapa_1["id"]


def test_enlace_cliente_rechaza_expiracion_mayor_a_365(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"expira_en_dias": 366},
    )
    assert respuesta.status_code == 422


def test_enlace_cliente_exige_seleccion_explicita_de_contenido(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"contenido": {}},
    )
    assert respuesta.status_code == 201
    assert respuesta.json()["contenido"] == {"conjunto_ids": [], "mapa_ids": []}
