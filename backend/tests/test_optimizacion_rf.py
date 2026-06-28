"""Pruebas del refinamiento RF de PB-07."""

import math
import tempfile

import pytest
from fastapi import HTTPException

from app.ai.modelo_propagacion import ModeloPropagacion, MuestraCalibracionRF
from app.ai.optimizador_ap_service import OptimizadorAPService
from app.api.v1.escenarios import _limite_aps_derivado, generar_conjuntos_ia
from app.api.v1.inventario_rf import crear_ap, obtener_inventario
from app.core.config import settings
from app.models.heatmap import ConjuntoAP, ConjuntoAPItem, MapaCalor
from app.models.medicion import MedicionWifi
from app.models.plano import Plano
from app.models.proyecto import Proyecto
from app.repositories.medicion_repository import MedicionRepository
from app.schemas.ia import RestriccionesIAIn
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
        poligono_interes=[
            {"x": 0, "y": 0},
            {"x": 400, "y": 0},
            {"x": 400, "y": 300},
            {"x": 0, "y": 300},
        ],
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


def _crear_conjunto_ap(
    db,
    *,
    plano: Plano,
    admin,
    nombre: str = "Conjunto IA prueba",
    proposito: str = "Validar conjunto completo de entrada",
    bssids: tuple[str, ...] = ("aa:bb:cc:dd:ee:24", "aa:bb:cc:dd:ee:50"),
) -> ConjuntoAP:
    conjunto = ConjuntoAP(
        plano_id=plano.id,
        nombre=nombre,
        proposito=proposito,
        origen="manual_web",
        creado_por_id=admin.id,
    )
    for bssid in bssids:
        conjunto.items.append(
            ConjuntoAPItem(
                bssid=bssid,
                ssid_snapshot="Bulldog-5" if bssid.endswith(":50") else "Bulldog-24",
                canal_snapshot=44 if bssid.endswith(":50") else 6,
                rssi_promedio_snapshot=-70,
            )
        )
    db.add(conjunto)
    db.commit()
    return conjunto


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


def test_limite_derivado_devuelve_top_3_recomendaciones():
    conjunto = ConjuntoAP(plano_id=1, nombre="Conjunto amplio", proposito="Top 3")
    for indice in range(5):
        conjunto.items.append(
            ConjuntoAPItem(
                bssid=f"aa:bb:cc:dd:ee:{indice:02x}",
                ssid_snapshot="LCM",
            )
        )

    assert (
        _limite_aps_derivado(
            conjunto_fuente=conjunto,
            bssids_seleccionados=None,
            aps_existentes=[],
        )
        == 3
    )


def test_optimizador_respeta_cantidad_de_mejores_recomendaciones():
    puntos = [
        PuntoRSSI(i, x, y, -82)
        for i, (x, y) in enumerate(
            ((20, 20), (380, 20), (20, 280), (380, 280), (200, 150), (120, 80)),
            start=1,
        )
    ]

    alternativas = OptimizadorAPService().optimizar(
        puntos_actuales=puntos,
        matriz_actual=[[-85.0] * 16 for _ in range(16)],
        ancho_px=400,
        alto_px=300,
        metros_por_pixel=0.1,
        max_aps=3,
        banda="5",
        bandas=["2.4", "5"],
        resolucion=16,
        umbral_objetivo_dbm=-70,
        cantidad_recomendaciones=2,
    )

    assert len(alternativas) == 2


def test_modelo_propagacion_calibra_parametros_locales_por_banda():
    muestras = [
        MuestraCalibracionRF(
            distancia_m=distancia,
            banda="5",
            rssi_dbm=-35 - 8 * math.log2(distancia) - 6.4,
        )
        for distancia in (1, 2, 4, 8, 16, 32)
    ]

    modelo = ModeloPropagacion.calibrar_desde_muestras(muestras)
    resumen = modelo.resumen_calibracion()
    prediccion = modelo.predecir_rssi(
        distancia_px=80,
        metros_por_pixel=0.1,
        banda="5",
    )

    assert resumen["tipo"] == "calibracion_local_por_plano"
    assert resumen["muestras"] == 6
    assert resumen["bandas"]["5"]["perdida_por_doble_distancia_db"] == pytest.approx(
        8.0,
        abs=0.1,
    )
    assert prediccion == pytest.approx(-65.4, abs=0.5)


def test_optimizador_dual_band_respeta_umbral_y_ap_fijo():
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
        banda="5",
        bandas=["2.4", "5"],
        resolucion=16,
        umbral_objetivo_dbm=-70,
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
    assert len(alternativas) == 3
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
    db_session, tecnico_usuario, admin_usuario, monkeypatch
):
    plano = _plano_con_mediciones(db_session, tecnico_usuario)
    originales = {
        medicion.id: medicion.rssi for medicion in db_session.query(MedicionWifi).all()
    }
    crear_ap(
        plano_id=plano.id,
        body=APFisicoCrearIn(
            nombre="AP existente calibracion",
            fabricante="Bulldog Tech.",
            modelo="BT-AX1800",
            coord_x=120,
            coord_y=100,
            altura_m=2.8,
            verificado=True,
            radios=[
                RadioAPIn(
                    banda="2.4",
                    canal=6,
                    potencia_original=8,
                    potencia_dbm=8,
                    potencia_max_dbm=20,
                    bssids=[
                        BSSIDRadioIn(
                            bssid="aa:bb:cc:dd:ee:24",
                            ssid="Bulldog-24",
                        )
                    ],
                ),
                RadioAPIn(
                    banda="5",
                    canal=44,
                    potencia_original=14,
                    potencia_dbm=14,
                    potencia_max_dbm=23,
                    bssids=[
                        BSSIDRadioIn(
                            bssid="aa:bb:cc:dd:ee:50",
                            ssid="Bulldog-5",
                        )
                    ],
                ),
            ],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )
    conjunto = _crear_conjunto_ap(
        db_session,
        plano=plano,
        admin=admin_usuario,
        nombre="Conjunto IA prueba",
        proposito="Validar APs detectados del mapa",
    )
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(settings, "storage_root", tmp)
        respuesta = generar_conjuntos_ia(
            proyecto_id=plano.proyecto_id,
            body=RestriccionesIAIn(
                bandas=["2.4", "5"],
                resolucion=32,
                umbral_objetivo_dbm=-70,
                fuente_entrada={
                    "tipo": "CONJUNTO_EXISTENTE",
                    "conjunto_id": conjunto.id,
                },
            ),
            request=None,
            db=db_session,
            current_user=admin_usuario,
        )
    assert len(respuesta.conjuntos) == 3
    conjunto_ia = respuesta.conjuntos[0]
    assert conjunto_ia.origen == "ia"
    assert conjunto_ia.conjunto_origen_id == conjunto.id
    assert conjunto_ia.creado_por_id == admin_usuario.id
    assert conjunto_ia.nombre == "Conjunto IA prueba · IA Propuesta 1"
    assert conjunto_ia.restricciones_ia["fuente_entrada"]["conjunto_id"] == conjunto.id
    assert conjunto_ia.restricciones_ia["limite_aps_derivado"] == 2
    assert set(conjunto_ia.restricciones_ia["fuente_entrada"]["bssids"]) == {
        "aa:bb:cc:dd:ee:24",
        "aa:bb:cc:dd:ee:50",
    }
    assert conjunto_ia.metricas_ia["calibracion_modelo"]["tipo"] == (
        "calibracion_local_por_plano"
    )
    assert conjunto_ia.metricas_ia["calibracion_modelo"]["muestras"] == 10
    assert set(conjunto_ia.metricas_ia["mapas_por_banda"]) == {"2.4", "5"}
    assert len(conjunto_ia.items[0].radios) == 2
    assert conjunto_ia.items[0].accion_recomendada in {
        "AGREGAR",
        "RECONFIGURAR",
        "MOVER",
    }
    db_session.expire_all()
    assert {
        medicion.id: medicion.rssi for medicion in db_session.query(MedicionWifi).all()
    } == originales
    assert len(conjunto_ia.metricas_ia["mapas_por_banda"]["5"]) == 32


def test_generacion_desde_conjunto_existente_conserva_fuente_y_bssids(
    db_session, tecnico_usuario, admin_usuario, monkeypatch
):
    plano = _plano_con_mediciones(db_session, tecnico_usuario)
    conjunto = _crear_conjunto_ap(
        db_session,
        plano=plano,
        admin=admin_usuario,
        nombre="Conjunto web 5 GHz",
        proposito="Optimizar la cobertura de la banda de 5 GHz",
        bssids=("aa:bb:cc:dd:ee:50",),
    )

    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(settings, "storage_root", tmp)
        respuesta = generar_conjuntos_ia(
            proyecto_id=plano.proyecto_id,
            body=RestriccionesIAIn(
                bandas=["5"],
                resolucion=32,
                fuente_entrada={
                    "tipo": "CONJUNTO_EXISTENTE",
                    "conjunto_id": conjunto.id,
                },
            ),
            request=None,
            db=db_session,
            current_user=admin_usuario,
        )
        segunda_respuesta = generar_conjuntos_ia(
            proyecto_id=plano.proyecto_id,
            body=RestriccionesIAIn(
                bandas=["5"],
                resolucion=32,
                fuente_entrada={
                    "tipo": "CONJUNTO_EXISTENTE",
                    "conjunto_id": conjunto.id,
                },
            ),
            request=None,
            db=db_session,
            current_user=admin_usuario,
        )

    conjunto_ia = respuesta.conjuntos[0]
    segundo_conjunto_ia = segunda_respuesta.conjuntos[0]
    assert conjunto_ia.nombre == "Conjunto web 5 GHz · IA Propuesta 1"
    assert conjunto_ia.conjunto_origen_id == conjunto.id
    assert segundo_conjunto_ia.nombre == "Conjunto web 5 GHz · IA Propuesta 1 (2)"
    assert conjunto_ia.restricciones_ia["fuente_entrada"]["conjunto_id"] == conjunto.id
    mapa_actual = (
        db_session.query(MapaCalor).filter_by(id=respuesta.mapa_actual.id).one()
    )
    mapa_proyectado = (
        db_session.query(MapaCalor)
        .filter_by(id=respuesta.mapas_proyectados[0].id)
        .one()
    )
    assert mapa_actual.conjunto_ap_id == conjunto.id
    assert mapa_proyectado.conjunto_ap_id == conjunto_ia.id
    assert conjunto_ia.origen == "ia"
    assert len(conjunto_ia.items) == conjunto_ia.cantidad_aps
    assert mapa_actual.bssids_generacion == ["aa:bb:cc:dd:ee:50"]


def test_ia_no_usa_conjunto_propuesto_por_ia_como_fuente(
    db_session,
    tecnico_usuario,
    admin_usuario,
):
    plano = _plano_con_mediciones(db_session, tecnico_usuario)
    conjunto_base = _crear_conjunto_ap(
        db_session,
        plano=plano,
        admin=admin_usuario,
        nombre="Conjunto técnico base",
        bssids=("aa:bb:cc:dd:ee:50",),
    )
    conjunto_ia = ConjuntoAP(
        plano_id=plano.id,
        conjunto_origen_id=conjunto_base.id,
        nombre="Conjunto IA derivado",
        proposito=conjunto_base.proposito,
        origen="ia",
        creado_por_id=admin_usuario.id,
    )
    conjunto_ia.items.append(
        ConjuntoAPItem(
            bssid="sp5:01:01:00:00",
            ssid_snapshot="AP recomendado",
            rssi_promedio_snapshot=-62,
        )
    )
    db_session.add(conjunto_ia)
    db_session.commit()

    with pytest.raises(HTTPException) as exc:
        generar_conjuntos_ia(
            proyecto_id=plano.proyecto_id,
            body=RestriccionesIAIn(
                bandas=["5"],
                resolucion=32,
                fuente_entrada={
                    "tipo": "CONJUNTO_EXISTENTE",
                    "conjunto_id": conjunto_ia.id,
                },
            ),
            request=None,
            db=db_session,
            current_user=admin_usuario,
        )

    assert exc.value.status_code == 422
    assert "conjunto técnico" in exc.value.detail


def test_tecnico_no_puede_generar_conjuntos_ia(db_session, tecnico_usuario):
    plano = _plano_con_mediciones(db_session, tecnico_usuario)
    conjunto = _crear_conjunto_ap(
        db_session,
        plano=plano,
        admin=tecnico_usuario,
        bssids=("aa:bb:cc:dd:ee:50",),
    )
    with pytest.raises(HTTPException) as exc:
        generar_conjuntos_ia(
            proyecto_id=plano.proyecto_id,
            body=RestriccionesIAIn(
                fuente_entrada={
                    "tipo": "CONJUNTO_EXISTENTE",
                    "conjunto_id": conjunto.id,
                }
            ),
            request=None,
            db=db_session,
            current_user=tecnico_usuario,
        )
    assert exc.value.status_code == 403
