"""Pruebas del refinamiento RF de PB-07/PB-12."""

import tempfile

from app.ai.modelo_propagacion import ModeloPropagacion
from app.ai.optimizador_ap_service import OptimizadorAPService
from app.api.v1.escenarios import generar_escenarios
from app.api.v1.inventario_rf import crear_ap, obtener_inventario
from app.core.config import settings
from app.models.medicion import MedicionWifi
from app.models.plano import Plano
from app.models.proyecto import Proyecto
from app.repositories.medicion_repository import MedicionRepository
from app.schemas.escenario import RestriccionesEscenarioIn
from app.schemas.inventario_rf import APFisicoCrearIn, BSSIDRadioIn, RadioAPIn
from app.schemas.medicion import MedicionItemIn
from app.services.interpolacion_service import PuntoRSSI


def _plano_con_mediciones(db, tecnico) -> Plano:
    proyecto = Proyecto(nombre="Optimización RF", tecnico_id=tecnico.id)
    db.add(proyecto)
    db.flush()
    plano = Plano(
        proyecto_id=proyecto.id,
        nombre="planta.png",
        formato="png",
        ruta_storage=f"rf/{proyecto.id}.png",
        ancho_px=400,
        alto_px=300,
        tamano_bytes=100,
        calibracion_x1=0,
        calibracion_y1=0,
        calibracion_x2=100,
        calibracion_y2=0,
        distancia_real_m=10,
        escala_m_por_px=0.1,
    )
    db.add(plano)
    db.commit()
    repo = MedicionRepository(db)
    for indice, (x, y) in enumerate(
        ((20, 20), (380, 20), (20, 280), (380, 280), (200, 150)), start=1
    ):
        repo.crear_lote(
            plano_id=plano.id,
            pos_x=x,
            pos_y=y,
            items=[
                MedicionItemIn(
                    ssid="Bulldog-24",
                    bssid="aa:bb:cc:dd:ee:24",
                    rssi=-55 - indice * 4,
                    canal=6,
                    frecuencia_mhz=2437,
                ),
                MedicionItemIn(
                    ssid="Bulldog-5",
                    bssid="aa:bb:cc:dd:ee:50",
                    rssi=-60 - indice * 5,
                    canal=44,
                    frecuencia_mhz=5220,
                ),
            ],
        )
    return plano


def test_propagacion_distingue_bandas_y_potencia():
    modelo = ModeloPropagacion()
    rssi_24 = modelo.predecir_rssi(
        distancia_px=100,
        metros_por_pixel=0.1,
        banda="2.4",
        potencia_dbm=8,
    )
    rssi_5 = modelo.predecir_rssi(
        distancia_px=100,
        metros_por_pixel=0.1,
        banda="5",
        potencia_dbm=8,
    )
    rssi_5_mayor_potencia = modelo.predecir_rssi(
        distancia_px=100,
        metros_por_pixel=0.1,
        banda="5",
        potencia_dbm=14,
    )
    assert rssi_24 > rssi_5
    assert rssi_5_mayor_potencia > rssi_5


def test_optimizador_dual_band_respeta_presupuesto_y_ap_fijo():
    puntos = [
        PuntoRSSI(i, x, y, -80)
        for i, (x, y) in enumerate(
            ((20, 20), (380, 20), (20, 280), (380, 280), (200, 150)), start=1
        )
    ]
    alternativas = OptimizadorAPService().optimizar(
        puntos_actuales=puntos,
        matriz_actual=[[-85.0] * 16 for _ in range(16)],
        ancho_px=400,
        alto_px=300,
        metros_por_pixel=0.1,
        max_aps=3,
        presupuesto=150,
        banda="5",
        bandas=["2.4", "5"],
        modelo_ap="AP de prueba",
        costo_unitario=100,
        resolucion=16,
        tipo_negocio="RED_EXISTENTE",
        aps_existentes=[
            {
                "id": 9,
                "coord_x": 55,
                "coord_y": 65,
                "altura_m": 3,
                "tipo_montaje": "TECHO",
                "restriccion_movimiento": "FIJO",
                "verificado": True,
            }
        ],
    )
    assert len(alternativas) == 1
    escenario = alternativas[0]
    assert set(escenario.mapas_por_banda) == {"2.4", "5"}
    assert escenario.recomendaciones[0]["coord_x"] == 55
    assert escenario.recomendaciones[0]["coord_y"] == 65
    assert escenario.recomendaciones[0]["accion"] == "RECONFIGURAR"
    assert len(escenario.recomendaciones[0]["radios"]) == 2


def test_inventario_modela_ap_radio_y_bssid(db_session, tecnico_usuario):
    plano = _plano_con_mediciones(db_session, tecnico_usuario)
    ap = crear_ap(
        plano_id=plano.id,
        body=APFisicoCrearIn(
            nombre="AP existente 1",
            fabricante="Bulldog Tech.",
            modelo="BT-AX1800",
            coord_x=100,
            coord_y=90,
            altura_m=2.8,
            verificado=True,
            radios=[
                RadioAPIn(
                    banda="2.4",
                    canal=6,
                    potencia_original=8,
                    potencia_dbm=8,
                    potencia_max_dbm=20,
                    bssids=[BSSIDRadioIn(bssid="aa:bb:cc:dd:ee:24", ssid="Bulldog-24")],
                ),
                RadioAPIn(
                    banda="5",
                    canal=44,
                    potencia_original=14,
                    potencia_dbm=14,
                    potencia_max_dbm=23,
                    bssids=[BSSIDRadioIn(bssid="aa:bb:cc:dd:ee:50", ssid="Bulldog-5")],
                ),
            ],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )
    inventario = obtener_inventario(
        plano_id=plano.id,
        db=db_session,
        current_user=tecnico_usuario,
    )
    assert ap.id
    assert len(inventario.aps[0].radios) == 2
    assert inventario.nivel_completitud == "ALTO"


def test_generacion_persiste_proyecciones_sin_alterar_mediciones(
    db_session, tecnico_usuario, monkeypatch
):
    plano = _plano_con_mediciones(db_session, tecnico_usuario)
    originales = {
        medicion.id: medicion.rssi for medicion in db_session.query(MedicionWifi).all()
    }
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(settings, "storage_root", tmp)
        respuesta = generar_escenarios(
            proyecto_id=plano.proyecto_id,
            body=RestriccionesEscenarioIn(
                max_aps=1,
                presupuesto=200,
                costo_unitario=100,
                bandas=["2.4", "5"],
                banda_preferida="5",
                resolucion=32,
            ),
            db=db_session,
            current_user=tecnico_usuario,
        )
    escenario = respuesta.escenarios[0]
    assert set(escenario.bandas) == {"2.4", "5"}
    assert set(escenario.mapas_por_banda) == {"2.4", "5"}
    assert set(escenario.mapas_actuales_por_banda) == {"2.4", "5"}
    assert escenario.mapas_actuales_por_banda["2.4"] is not None
    assert escenario.mapas_actuales_por_banda["5"] is not None
    assert len(escenario.recomendaciones[0].radios) == 2
    db_session.expire_all()
    assert {
        medicion.id: medicion.rssi for medicion in db_session.query(MedicionWifi).all()
    } == originales
    assert len(escenario.mapas_por_banda["5"]) == 32
