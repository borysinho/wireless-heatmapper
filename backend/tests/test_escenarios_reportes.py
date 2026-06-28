"""Tests Sprint 5 — PB-07."""

import pytest

from app.ai.modelo_propagacion import ModeloPropagacion
from app.ai.optimizador_ap_service import OptimizadorAPService
from app.services.interpolacion_service import PuntoRSSI


def test_fspl_pierde_seis_db_por_duplicar_distancia():
    modelo = ModeloPropagacion()
    rssi_1m = modelo.fspl(distancia_m=1)
    rssi_2m = modelo.fspl(distancia_m=2)
    rssi_4m = modelo.fspl(distancia_m=4)
    assert rssi_2m == pytest.approx(rssi_1m - 6, abs=0.1)
    assert rssi_4m == pytest.approx(rssi_2m - 6, abs=0.1)


def test_optimizador_edificio_en_u_propone_aps_en_extremos():
    puntos = [
        PuntoRSSI(punto_id=1, x=20, y=20, rssi=-91),
        PuntoRSSI(punto_id=2, x=380, y=20, rssi=-92),
        PuntoRSSI(punto_id=3, x=20, y=280, rssi=-88),
        PuntoRSSI(punto_id=4, x=380, y=280, rssi=-89),
        PuntoRSSI(punto_id=5, x=200, y=150, rssi=-76),
        PuntoRSSI(punto_id=6, x=200, y=40, rssi=-80),
    ]
    matriz_actual = [[-85.0 for _ in range(32)] for _ in range(32)]

    escenarios = OptimizadorAPService().optimizar(
        puntos_actuales=puntos,
        matriz_actual=matriz_actual,
        ancho_px=400,
        alto_px=300,
        metros_por_pixel=0.1,
        max_aps=2,
        banda="5",
        resolucion=32,
        umbral_objetivo_dbm=-70,
    )

    assert escenarios
    assert len(escenarios) == 3
    mejor = escenarios[0]
    assert mejor.cantidad_aps <= 2
    assert mejor.pct_cobertura >= mejor.pct_cobertura_actual
    xs = [rec["coord_x"] for rec in mejor.recomendaciones]
    assert min(xs) < 120 or max(xs) > 280
    assert "RSSI proyectado" in mejor.recomendaciones[0]["justificacion"]
    assert "potencia TX ajustable" in mejor.recomendaciones[0]["justificacion"]


def test_optimizador_respeta_poligono_de_interes():
    puntos = [
        PuntoRSSI(punto_id=1, x=40, y=40, rssi=-94),
        PuntoRSSI(punto_id=2, x=80, y=260, rssi=-92),
        PuntoRSSI(punto_id=3, x=230, y=40, rssi=-85),
        PuntoRSSI(punto_id=4, x=360, y=260, rssi=-88),
        PuntoRSSI(punto_id=5, x=300, y=150, rssi=-82),
    ]
    poligono = [
        {"x": 200, "y": 0},
        {"x": 400, "y": 0},
        {"x": 400, "y": 300},
        {"x": 200, "y": 300},
    ]

    escenarios = OptimizadorAPService().optimizar(
        puntos_actuales=puntos,
        matriz_actual=[[-90.0 for _ in range(32)] for _ in range(32)],
        ancho_px=400,
        alto_px=300,
        metros_por_pixel=0.1,
        max_aps=2,
        banda="5",
        resolucion=32,
        umbral_objetivo_dbm=-70,
        poligono_interes=poligono,
    )

    for recomendacion in escenarios[0].recomendaciones:
        assert recomendacion["coord_x"] >= 200
        assert 0 <= recomendacion["coord_y"] <= 300
