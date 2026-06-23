"""Tests Sprint 6 — PB-15, PB-16 y PB-17."""

from datetime import UTC, datetime, timedelta

from app.core.config import settings
from app.models.escenario import EscenarioOptimizado, RecomendacionAP, Reporte
from app.models.heatmap import (
    AnalisisCobertura,
    APDetectado,
    ConjuntoAP,
    ConjuntoAPItem,
    MapaCalor,
)
from app.models.cliente import Cliente
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
    db.flush()
    analisis = AnalisisCobertura(
        mapa_calor_id=mapa.id,
        pct_cobertura=92.5,
        pct_zonas_muertas=0,
        celdas_zonas_muertas=0,
        cantidad_solapamientos=1,
        cantidad_interferencias=0,
        hallazgos={"zonas_muertas": []},
        resumen="Cobertura apta para el cliente.",
    )
    db.add(analisis)
    db.flush()
    db.add(
        APDetectado(
            analisis_id=analisis.id,
            bssid="aa:bb:cc:dd:ee:01",
            ssid="BulldogCorp",
            canal=6,
            frecuencia_mhz=2437,
            rssi_promedio=-62,
            pos_x=100,
            pos_y=120,
            confirmado=True,
        )
    )
    escenario = EscenarioOptimizado(
        proyecto_id=proyecto.id,
        plano_id=plano.id,
        mapa_actual_id=mapa.id,
        mapa_proyectado_id=mapa.id,
        origen="ia",
        estado_gobernanza="publicado_cliente",
        nombre="Alternativa publicada",
        banda="5",
        bandas=["5"],
        modelo_ap="AP propuesto para cobertura",
        pct_cobertura_actual=80,
        pct_cobertura=95,
        costo_estimado=0,
        cantidad_aps=1,
        resumen="Mejora publicada para cliente.",
        restricciones={"max_aps": 1},
        metricas={"mejora_pct": 15},
        mapas_por_banda={},
        mapas_actuales_por_banda={},
    )
    db.add(escenario)
    db.flush()
    db.add(
        RecomendacionAP(
            escenario_id=escenario.id,
            orden=1,
            accion="AGREGAR",
            coord_x=180,
            coord_y=140,
            altura_m=2.8,
            tipo_montaje="TECHO",
            banda="5",
            modelo_ap="AP propuesto para cobertura",
            costo_estimado=120,
            rssi_proyectado=-64,
            radios=[{"banda": "5", "canal": 44}],
            justificacion="Refuerza la cobertura en el ala norte.",
        )
    )
    reporte = Reporte(
        proyecto_id=proyecto.id,
        escenario=escenario,
        estado="LISTO",
        ruta_pdf=f"reportes/proyecto_{proyecto.id}/reporte.pdf",
        sha256="a" * 64,
        tamanio_bytes=120,
    )
    db.add(reporte)
    db.commit()
    db.refresh(proyecto)
    db.refresh(mapa)
    db.refresh(analisis)
    db.refresh(escenario)
    db.refresh(reporte)
    return proyecto, mapa, analisis, escenario, reporte


def _crear_conjunto_publicado_con_mediciones(db, proyecto):
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
        nombre="Conjunto publicado",
        proposito="Cobertura cliente",
        origen="manual_web",
        estado_gobernanza="publicado_cliente",
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
    proyecto, mapa, analisis, escenario, reporte = _crear_proyecto_publicable(
        db_session,
        tecnico_usuario,
    )

    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "expira_en_dias": 7,
            "contenido": {
                "mapa_ids": [mapa.id],
                "analisis_ids": [analisis.id],
                "escenario_ids": [escenario.id],
                "reporte_id": reporte.id,
            },
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
    assert payload["proyecto"].get("tecnico") is None
    assert [item["id"] for item in payload["heatmaps"]] == [mapa.id]
    assert [item["id"] for item in payload["analisis"]] == [analisis.id]
    assert [item["id"] for item in payload["escenarios"]] == [escenario.id]
    assert payload["reporte_disponible"] is True

    db_session.expire_all()
    enlace_db = db_session.query(TokenEnlaceCliente).filter_by(id=enlace["id"]).one()
    assert enlace_db.accesos == 1
    assert enlace_db.ultimo_acceso is not None

    reporte_response = client.get(f"/share/{token}/reporte", follow_redirects=False)
    assert reporte_response.status_code == 302
    assert "/reportes/archivo/" in reporte_response.headers["location"]


def test_enlace_cliente_envia_correo_al_cliente_seleccionado(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
    monkeypatch,
):
    proyecto, mapa, _, _, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
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
    proyecto, mapa, _, _, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
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
    assert (
        respuesta.json()["detail"]
        == "El correo transaccional no está configurado."
    )
    assert db_session.query(TokenEnlaceCliente).count() == 0


def test_enlace_generado_puede_enviarse_por_correo(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
    monkeypatch,
):
    proyecto, mapa, _, _, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
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
        json={
            "expira_en_dias": 7,
            "contenido": {"mapa_ids": [mapa.id]},
        },
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
    assert envios[0]["url_publica"].startswith("http://testserver/portal/")


def test_enlace_generado_no_envia_correo_si_esta_revocado(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, mapa, _, _, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
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
        json={
            "expira_en_dias": 7,
            "contenido": {"mapa_ids": [mapa.id]},
        },
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
    proyecto, mapa, _, _, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
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
    proyecto, mapa, _, _, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
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


def test_enlace_cliente_rechaza_escenario_no_publicado(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, _, _, escenario, _ = _crear_proyecto_publicable(
        db_session,
        tecnico_usuario,
    )
    escenario.estado_gobernanza = "aprobado_interno"
    db_session.commit()

    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "expira_en_dias": 7,
            "contenido": {"escenario_ids": [escenario.id]},
        },
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"] == "Escenario no publicado para cliente."


def test_enlace_deja_de_exponer_escenario_si_se_retira_publicacion(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, _, _, escenario, _ = _crear_proyecto_publicable(
        db_session, tecnico_usuario
    )
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"contenido": {"escenario_ids": [escenario.id]}},
    )
    assert respuesta.status_code == 201
    token = respuesta.json()["url_publica"].removeprefix("/portal/")

    escenario.estado_gobernanza = "aprobado_interno"
    db_session.commit()

    portal = client.get(f"/share/{token}")
    assert portal.status_code == 200
    assert portal.json()["escenarios"] == []


def test_enlace_con_solo_escenario_ia_expone_plano_y_recomendaciones(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, _, _, escenario, _ = _crear_proyecto_publicable(
        db_session, tecnico_usuario
    )
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"contenido": {"escenario_ids": [escenario.id]}},
    )
    assert respuesta.status_code == 201
    token = respuesta.json()["url_publica"].removeprefix("/portal/")

    portal = client.get(f"/share/{token}")

    assert portal.status_code == 200
    payload = portal.json()
    assert [item["id"] for item in payload["planos"]] == [escenario.plano_id]
    assert [item["id"] for item in payload["heatmaps"]] == [escenario.mapa_proyectado_id]
    assert [item["id"] for item in payload["escenarios"]] == [escenario.id]
    recomendaciones = payload["escenarios"][0]["recomendaciones"]
    assert len(recomendaciones) == 1
    assert recomendaciones[0]["accion"] == "AGREGAR"
    assert recomendaciones[0]["justificacion"] == "Refuerza la cobertura en el ala norte."


def test_enlace_con_contenido_explicito_no_agrega_reporte_automaticamente(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
):
    proyecto, mapa, _, _, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"contenido": {"mapa_ids": [mapa.id]}},
    )

    assert respuesta.status_code == 201
    assert respuesta.json()["contenido"]["reporte_id"] is None


def test_portal_genera_heatmap_desde_conjunto_y_reutiliza_cache(
    client,
    db_session,
    admin_token,
    tecnico_usuario,
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(settings, "storage_root", str(tmp_path))
    monkeypatch.setattr(settings, "storage_url_secret", "test_secret_32chars_minimo_xxxxxx")
    proyecto, _, _, _, _ = _crear_proyecto_publicable(db_session, tecnico_usuario)
    conjunto = _crear_conjunto_publicado_con_mediciones(db_session, proyecto)
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
    proyecto, *_ = _crear_proyecto_publicable(db_session, tecnico_usuario)
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
    proyecto, *_ = _crear_proyecto_publicable(db_session, tecnico_usuario)
    respuesta = client.post(
        f"/share/proyectos/{proyecto.id}/enlaces",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"expira_en_dias": 7},
    )

    assert respuesta.status_code == 422
