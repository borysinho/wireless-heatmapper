"""Tests Sprint 4 — PB-05 (Heatmap) y PB-06 (Análisis de cobertura)."""

import tempfile
import time
from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException

from app.api.v1.heatmaps import (
    _resolver_aps_interes,
    actualizar_conjunto_ap,
    actualizar_ubicacion_ap_conjunto,
    crear_conjunto_ap,
    generar_heatmap,
    generar_heatmap_conjunto,
    generar_heatmaps_faltantes_conjunto,
    listar_aps_disponibles,
    listar_conjuntos_ap,
)
from app.core.config import settings
from app.models.heatmap import ConjuntoAP, ConjuntoAPItem, MapaCalor
from app.models.medicion import LecturaRSSI
from app.models.plano import Plano
from app.models.proyecto import Proyecto
from app.models.share import TokenEnlaceCliente
from app.repositories.heatmap_repository import MapaCalorRepository
from app.repositories.medicion_repository import ORIGEN_IA_ESTIMADA, MedicionRepository
from app.schemas.heatmap import (
    ActualizarUbicacionAPConjuntoIn,
    ConjuntoAPActualizarIn,
    ConjuntoAPCrearIn,
    GenerarHeatmapConjuntoIn,
    GenerarHeatmapsFaltantesIn,
)
from app.schemas.medicion import MedicionItemIn
from app.services.interpolacion_service import (
    ESCALA_CWNA,
    HeatmapImageService,
    InterpolacionService,
    PuntoRSSI,
)


@pytest.fixture(autouse=True)
def storage_temporal(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(settings, "storage_root", tmp)
        monkeypatch.setattr(
            settings,
            "storage_url_secret",
            "test_secret_32chars_minimo_xxxxxx",
        )
        monkeypatch.setattr(settings, "storage_url_ttl_seconds", 60)
        monkeypatch.setattr(settings, "public_api_url", "")
        yield tmp


def _crear_plano_calibrado(db_session, tecnico_usuario) -> int:
    proyecto = Proyecto(
        nombre="Proyecto Heatmap",
        tecnico_id=tecnico_usuario.id,
    )
    db_session.add(proyecto)
    db_session.flush()

    plano = Plano(
        proyecto_id=proyecto.id,
        nombre="planta.png",
        formato="png",
        ruta_storage=f"{proyecto.id}/planta.png",
        ancho_px=400,
        alto_px=300,
        tamano_bytes=1024,
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
    db_session.add(plano)
    db_session.commit()
    return plano.id


def _insertar_puntos_sinteticos(db_session, plano_id: int, *, cantidad: int = 5):
    coords = [
        (20, 20, -45),
        (380, 20, -62),
        (20, 280, -74),
        (380, 280, -88),
        (200, 150, -92),
        (200, 40, -58),
        (80, 160, -69),
        (330, 170, -77),
    ]
    repo = MedicionRepository(db_session)
    for x, y, rssi_base in coords[:cantidad]:
        repo.crear_lote(
            plano_id=plano_id,
            pos_x=x,
            pos_y=y,
            items=[
                MedicionItemIn(
                    ssid="BulldogCorp",
                    bssid="aa:bb:cc:dd:ee:01",
                    rssi=rssi_base,
                    canal=6,
                    frecuencia_mhz=2437,
                ),
                MedicionItemIn(
                    ssid="BulldogCorp",
                    bssid="aa:bb:cc:dd:ee:02",
                    rssi=min(-40, rssi_base + 4),
                    canal=6,
                    frecuencia_mhz=2437,
                ),
                MedicionItemIn(
                    ssid="Invitados",
                    bssid="aa:bb:cc:dd:ee:03",
                    rssi=min(-42, rssi_base + 6),
                    canal=9,
                    frecuencia_mhz=2452,
                ),
            ],
        )


def test_invalidar_plano_elimina_conjuntos_ia_y_mapas_derivados(
    db_session,
    tecnico_usuario,
    admin_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)
    punto = db_session.query(LecturaRSSI).first().punto
    conjunto_ia = ConjuntoAP(
        plano_id=plano_id,
        nombre="Propuesta IA obsoleta",
        proposito="Debe eliminarse si cambian las mediciones.",
        origen="ia",
        creado_por_id=admin_usuario.id,
    )
    conjunto_ia.items.append(
        ConjuntoAPItem(
            bssid="sp5:99:01:00:00",
            ssid_snapshot="AP recomendado",
            pos_x=120,
            pos_y=90,
            banda="5",
        )
    )
    db_session.add(conjunto_ia)
    db_session.flush()
    db_session.add(
        LecturaRSSI(
            punto_id=punto.id,
            ssid="AP recomendado",
            bssid="sp5:99:01:00:00",
            rssi=-62,
            canal=36,
            frecuencia_mhz=5180,
            nivel="verde",
            numero_lectura=1,
            origen=ORIGEN_IA_ESTIMADA,
            conjunto_ap_id=conjunto_ia.id,
            modelo_origen="rf-hibrido-1.1",
            incertidumbre_db=6.0,
        )
    )
    for idx, conjunto_ap_id in enumerate((None, conjunto_ia.id), start=1):
        db_session.add(
            MapaCalor(
                plano_id=plano_id,
                conjunto_ap_id=conjunto_ap_id,
                algoritmo="IDW",
                resolucion=64,
                modo_generacion="PROYECTADO" if conjunto_ap_id else "SUBCONJUNTO",
                bssid="sp5:99:01:00:00",
                ssid="AP recomendado",
                ap_pos_x=120,
                ap_pos_y=90,
                aps_interes=[],
                bssids_generacion=["sp5:99:01:00:00"],
                matriz=[[-62.0]],
                escala=ESCALA_CWNA,
                ruta_imagen=f"heatmaps/invalidacion-{idx}.png",
                cantidad_puntos=1,
                rssi_min=-62,
                rssi_max=-62,
                firma_mediciones=f"firma-invalidacion-{idx}",
            )
        )
    db_session.commit()

    MapaCalorRepository(db_session).invalidar_plano(plano_id=plano_id)
    db_session.commit()

    assert db_session.query(ConjuntoAP).filter_by(id=conjunto_ia.id).first() is None
    assert (
        db_session.query(LecturaRSSI)
        .filter(
            LecturaRSSI.origen == ORIGEN_IA_ESTIMADA,
            LecturaRSSI.conjunto_ap_id == conjunto_ia.id,
        )
        .count()
        == 0
    )
    assert db_session.query(MapaCalor).filter_by(plano_id=plano_id).count() == 0


def test_heatmap_requiere_minimo_cinco_puntos(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=4)

    with pytest.raises(HTTPException) as exc:
        generar_heatmap(
            plano_id=plano_id,
            request=None,
            bssid=["aa:bb:cc:dd:ee:01"],
            ap_pos_x=[100],
            ap_pos_y=[100],
            algoritmo="IDW",
            resolucion=64,
            db=db_session,
            current_user=tecnico_usuario,
        )

    assert exc.value.status_code == 422
    assert "Se requieren al menos 5 puntos de los APs seleccionados" in exc.value.detail


def test_listar_aps_disponibles_para_seleccion(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)

    aps = listar_aps_disponibles(
        plano_id=plano_id,
        db=db_session,
        current_user=tecnico_usuario,
    )

    assert len(aps) == 3
    assert aps[0].bssid == "aa:bb:cc:dd:ee:03"
    assert aps[0].cantidad_puntos == 5
    assert all(not ap.seleccionado for ap in aps)


def test_crear_conjunto_ap_acepta_proposito_vacio(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)

    conjunto = crear_conjunto_ap(
        plano_id=plano_id,
        body=ConjuntoAPCrearIn(
            nombre="Red corporativa",
            proposito="",
            banda_objetivo="2.4",
            bssids=["aa:bb:cc:dd:ee:01"],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )

    assert conjunto.nombre == "Red corporativa"
    assert conjunto.proposito == ""
    assert conjunto.banda_objetivo == "2.4"
    assert conjunto.cantidad_aps == 1


def test_crear_conjunto_ap_rechaza_aps_fuera_de_banda(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)

    with pytest.raises(HTTPException) as exc:
        crear_conjunto_ap(
            plano_id=plano_id,
            body=ConjuntoAPCrearIn(
                nombre="Red corporativa",
                proposito="Validar banda objetivo.",
                banda_objetivo="5",
                bssids=["aa:bb:cc:dd:ee:01"],
            ),
            db=db_session,
            current_user=tecnico_usuario,
        )

    assert exc.value.status_code == 422
    assert "no pertenecen a la banda 5 GHz" in exc.value.detail


def test_crear_conjunto_ap_y_generar_heatmaps_por_modo(
    db_session,
    tecnico_usuario,
    admin_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)

    conjunto = crear_conjunto_ap(
        plano_id=plano_id,
        body=ConjuntoAPCrearIn(
            nombre="Red corporativa",
            proposito="Evaluar cobertura principal de Bulldog Tech.",
            banda_objetivo="2.4",
            bssids=["aa:bb:cc:dd:ee:01", "aa:bb:cc:dd:ee:02"],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )

    assert conjunto.nombre == "Red corporativa"
    assert conjunto.origen == "manual_movil"
    assert conjunto.banda_objetivo == "2.4"
    assert conjunto.creado_por_id == tecnico_usuario.id
    assert conjunto.cantidad_aps == 2
    assert [item.bssid for item in conjunto.items] == [
        "aa:bb:cc:dd:ee:01",
        "aa:bb:cc:dd:ee:02",
    ]
    assert (
        listar_conjuntos_ap(
            plano_id=plano_id,
            db=db_session,
            current_user=tecnico_usuario,
        )[0].id
        == conjunto.id
    )

    revisado = actualizar_conjunto_ap(
        conjunto_id=conjunto.id,
        body=ConjuntoAPActualizarIn(descripcion="Selección técnica validada."),
        db=db_session,
        current_user=admin_usuario,
    )
    assert revisado.descripcion == "Selección técnica validada."

    mapa_completo = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(modo="CONJUNTO_COMPLETO", resolucion=64),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )
    mapa_individual = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(
            modo="INDIVIDUAL",
            bssids=["aa:bb:cc:dd:ee:01"],
            resolucion=64,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )
    mapa_subconjunto = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(
            modo="SUBCONJUNTO",
            bssids=["aa:bb:cc:dd:ee:02"],
            resolucion=64,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )

    assert mapa_completo.conjunto_ap_id == conjunto.id
    assert mapa_completo.modo_generacion == "CONJUNTO_COMPLETO"
    assert mapa_completo.bssids_generacion == [
        "aa:bb:cc:dd:ee:01",
        "aa:bb:cc:dd:ee:02",
    ]
    assert mapa_individual.modo_generacion == "INDIVIDUAL"
    assert mapa_individual.bssids_generacion == ["aa:bb:cc:dd:ee:01"]
    assert mapa_subconjunto.modo_generacion == "SUBCONJUNTO"
    assert mapa_subconjunto.bssids_generacion == ["aa:bb:cc:dd:ee:02"]


def test_generar_heatmaps_faltantes_actualiza_idw(
    db_session,
    tecnico_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)
    conjunto = crear_conjunto_ap(
        plano_id=plano_id,
        body=ConjuntoAPCrearIn(
            nombre="Cobertura campo",
            proposito="Validar actualización de mapas globales e individuales.",
            banda_objetivo="2.4",
            bssids=[
                "aa:bb:cc:dd:ee:01",
                "aa:bb:cc:dd:ee:02",
                "aa:bb:cc:dd:ee:03",
            ],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )
    mapa_previo = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(
            modo="CONJUNTO_COMPLETO",
            algoritmo="IDW",
            resolucion=64,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )
    plano = db_session.query(Plano).filter(Plano.id == plano_id).one()
    enlace = TokenEnlaceCliente(
        proyecto_id=plano.proyecto_id,
        token="portal-actualizacion-idw",
        contenido={"mapa_ids": [mapa_previo.id]},
        expira_en=datetime.now(UTC) + timedelta(days=7),
        creado_por_id=tecnico_usuario.id,
    )
    db_session.add(enlace)
    db_session.commit()

    generados = generar_heatmaps_faltantes_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapsFaltantesIn(
            algoritmo="IDW",
            resolucion=64,
            actualizar_existentes=True,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )

    mapas = (
        db_session.query(MapaCalor)
        .filter(MapaCalor.conjunto_ap_id == conjunto.id)
        .all()
    )
    claves_esperadas = {
        ("aa:bb:cc:dd:ee:01",),
        ("aa:bb:cc:dd:ee:02",),
        ("aa:bb:cc:dd:ee:03",),
        (
            "aa:bb:cc:dd:ee:01",
            "aa:bb:cc:dd:ee:02",
            "aa:bb:cc:dd:ee:03",
        ),
    }
    assert len(generados) == 4
    assert len(mapas) == 4
    assert mapa_previo.id not in {mapa.id for mapa in mapas}
    assert {mapa.algoritmo for mapa in mapas} == {"IDW"}
    assert {mapa.modo_generacion for mapa in mapas} == {
        "CONJUNTO_COMPLETO",
        "INDIVIDUAL",
    }
    claves_algoritmo = {tuple(sorted(mapa.bssids_generacion)) for mapa in mapas}
    assert claves_algoritmo == claves_esperadas
    mapa_global = next(
        mapa
        for mapa in mapas
        if tuple(sorted(mapa.bssids_generacion))
        == (
            "aa:bb:cc:dd:ee:01",
            "aa:bb:cc:dd:ee:02",
            "aa:bb:cc:dd:ee:03",
        )
    )
    db_session.refresh(enlace)
    assert enlace.contenido["mapa_ids"] == [mapa_global.id]


def test_generar_heatmaps_faltantes_agrega_mapas_a_enlace_con_conjunto(
    db_session,
    tecnico_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)
    conjunto = crear_conjunto_ap(
        plano_id=plano_id,
        body=ConjuntoAPCrearIn(
            nombre="Cobertura portal",
            proposito="Validar portal con conjunto publicado.",
            banda_objetivo="2.4",
            bssids=[
                "aa:bb:cc:dd:ee:01",
                "aa:bb:cc:dd:ee:02",
                "aa:bb:cc:dd:ee:03",
            ],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )
    mapa_previo = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(
            modo="CONJUNTO_COMPLETO",
            algoritmo="IDW",
            resolucion=64,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )
    plano = db_session.query(Plano).filter(Plano.id == plano_id).one()
    enlace = TokenEnlaceCliente(
        proyecto_id=plano.proyecto_id,
        token="portal-conjunto-faltantes-idw",
        contenido={
            "conjunto_ids": [conjunto.id],
            "mapa_ids": [mapa_previo.id],
        },
        expira_en=datetime.now(UTC) + timedelta(days=7),
        creado_por_id=tecnico_usuario.id,
    )
    db_session.add(enlace)
    db_session.commit()

    generar_heatmaps_faltantes_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapsFaltantesIn(
            algoritmo="IDW",
            resolucion=64,
            actualizar_existentes=True,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )

    mapas = (
        db_session.query(MapaCalor)
        .filter(MapaCalor.conjunto_ap_id == conjunto.id)
        .all()
    )
    db_session.refresh(enlace)

    assert len(mapas) == 4
    assert enlace.contenido["conjunto_ids"] == [conjunto.id]
    assert set(enlace.contenido["mapa_ids"]) == {mapa.id for mapa in mapas}


def test_generar_heatmaps_faltantes_reemplaza_todos_los_previos_del_conjunto(
    db_session,
    tecnico_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)
    conjunto = crear_conjunto_ap(
        plano_id=plano_id,
        body=ConjuntoAPCrearIn(
            nombre="Cobertura cliente",
            proposito="Validar reemplazo total desde previsualización.",
            banda_objetivo="2.4",
            bssids=[
                "aa:bb:cc:dd:ee:01",
                "aa:bb:cc:dd:ee:02",
            ],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )
    mapa_64 = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(
            modo="CONJUNTO_COMPLETO",
            algoritmo="IDW",
            resolucion=64,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )
    mapa_128 = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(
            modo="INDIVIDUAL",
            bssids=["aa:bb:cc:dd:ee:01"],
            algoritmo="IDW",
            resolucion=128,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )
    plano = db_session.query(Plano).filter(Plano.id == plano_id).one()
    enlace = TokenEnlaceCliente(
        proyecto_id=plano.proyecto_id,
        token="portal-reemplazo-idw",
        contenido={"mapa_ids": [mapa_64.id, mapa_128.id]},
        expira_en=datetime.now(UTC) + timedelta(days=7),
        creado_por_id=tecnico_usuario.id,
    )
    db_session.add(enlace)
    db_session.commit()

    generados = generar_heatmaps_faltantes_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapsFaltantesIn(
            algoritmo="IDW",
            resolucion=64,
            actualizar_existentes=True,
            reemplazar_existentes=True,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )

    mapas = (
        db_session.query(MapaCalor)
        .filter(MapaCalor.conjunto_ap_id == conjunto.id)
        .all()
    )

    assert len(generados) == 3
    assert len(mapas) == 3
    assert {mapa_64.id, mapa_128.id}.isdisjoint({mapa.id for mapa in mapas})
    assert {mapa.resolucion for mapa in mapas} == {64}
    assert {mapa.modo_generacion for mapa in mapas} == {
        "CONJUNTO_COMPLETO",
        "INDIVIDUAL",
    }
    mapa_global = next(
        mapa
        for mapa in mapas
        if tuple(sorted(mapa.bssids_generacion))
        == ("aa:bb:cc:dd:ee:01", "aa:bb:cc:dd:ee:02")
    )
    mapa_individual = next(
        mapa
        for mapa in mapas
        if tuple(sorted(mapa.bssids_generacion)) == ("aa:bb:cc:dd:ee:01",)
    )
    db_session.refresh(enlace)
    assert enlace.contenido["mapa_ids"] == [mapa_global.id, mapa_individual.id]


def test_generar_heatmaps_faltantes_ia_reconstruye_lecturas_para_idw(
    db_session,
    tecnico_usuario,
    admin_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)
    conjunto = ConjuntoAP(
        plano_id=plano_id,
        nombre="Propuesta IA heredada",
        proposito="Validar mapas IDW de recomendaciones IA.",
        banda_objetivo="2.4",
        origen="ia",
        creado_por_id=admin_usuario.id,
    )
    conjunto.items.extend(
        [
            ConjuntoAPItem(
                bssid="sp5:01:01:00:00",
                ssid_snapshot="AP recomendado 1",
                canal_snapshot=6,
                rssi_promedio_snapshot=-62,
                pos_x=120,
                pos_y=90,
                banda="2.4",
                radios=[{"potencia_dbm": 14, "ganancia_dbi": 3}],
            ),
            ConjuntoAPItem(
                bssid="sp5:01:02:00:00",
                ssid_snapshot="AP recomendado 2",
                canal_snapshot=11,
                rssi_promedio_snapshot=-64,
                pos_x=300,
                pos_y=210,
                banda="2.4",
                radios=[{"potencia_dbm": 14, "ganancia_dbi": 3}],
            ),
        ]
    )
    db_session.add(conjunto)
    db_session.commit()

    assert (
        db_session.query(LecturaRSSI)
        .filter(
            LecturaRSSI.origen == ORIGEN_IA_ESTIMADA,
            LecturaRSSI.conjunto_ap_id == conjunto.id,
        )
        .count()
        == 0
    )

    generados = generar_heatmaps_faltantes_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapsFaltantesIn(
            algoritmo="IDW",
            resolucion=64,
            actualizar_existentes=True,
        ),
        request=None,
        db=db_session,
        current_user=admin_usuario,
    )

    assert len(generados) == 3
    assert {mapa.algoritmo for mapa in generados} == {"IDW"}
    assert {mapa.modo_generacion for mapa in generados} == {
        "PROYECTADO",
        "INDIVIDUAL",
    }
    assert (
        db_session.query(LecturaRSSI)
        .filter(
            LecturaRSSI.origen == ORIGEN_IA_ESTIMADA,
            LecturaRSSI.conjunto_ap_id == conjunto.id,
        )
        .count()
        == 10
    )


def test_generar_heatmaps_faltantes_ia_desde_un_solo_mapa_existente(
    db_session,
    tecnico_usuario,
    admin_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)
    conjunto = ConjuntoAP(
        plano_id=plano_id,
        nombre="Propuesta IA con mapa único",
        proposito="Completar mapa global e individuales desde el mapa inicial.",
        banda_objetivo="2.4",
        origen="ia",
        creado_por_id=admin_usuario.id,
    )
    conjunto.items.extend(
        [
            ConjuntoAPItem(
                bssid="sp5:02:01:00:00",
                ssid_snapshot="AP recomendado 1",
                canal_snapshot=1,
                rssi_promedio_snapshot=-62,
                pos_x=120,
                pos_y=90,
                banda="2.4",
                radios=[{"potencia_dbm": 14, "ganancia_dbi": 3}],
            ),
            ConjuntoAPItem(
                bssid="sp5:02:02:00:00",
                ssid_snapshot="AP recomendado 2",
                canal_snapshot=6,
                rssi_promedio_snapshot=-64,
                pos_x=260,
                pos_y=160,
                banda="2.4",
                radios=[{"potencia_dbm": 14, "ganancia_dbi": 3}],
            ),
            ConjuntoAPItem(
                bssid="sp5:02:03:00:00",
                ssid_snapshot="AP recomendado 3",
                canal_snapshot=11,
                rssi_promedio_snapshot=-65,
                pos_x=340,
                pos_y=230,
                banda="2.4",
                radios=[{"potencia_dbm": 14, "ganancia_dbi": 3}],
            ),
        ]
    )
    db_session.add(conjunto)
    db_session.commit()

    mapa_inicial = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(
            modo="CONJUNTO_COMPLETO",
            algoritmo="IDW",
            resolucion=64,
        ),
        request=None,
        db=db_session,
        current_user=admin_usuario,
    )

    assert (
        db_session.query(MapaCalor)
        .filter(MapaCalor.conjunto_ap_id == conjunto.id)
        .count()
        == 1
    )

    generados = generar_heatmaps_faltantes_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapsFaltantesIn(
            algoritmo="IDW",
            resolucion=64,
            actualizar_existentes=True,
        ),
        request=None,
        db=db_session,
        current_user=admin_usuario,
    )

    mapas = (
        db_session.query(MapaCalor)
        .filter(MapaCalor.conjunto_ap_id == conjunto.id)
        .all()
    )
    assert len(generados) == 4
    assert len(mapas) == 4
    assert mapa_inicial.id not in {mapa.id for mapa in mapas}
    assert {mapa.algoritmo for mapa in mapas} == {"IDW"}
    assert {mapa.modo_generacion for mapa in mapas} == {
        "PROYECTADO",
        "INDIVIDUAL",
    }
    assert {
        (mapa.algoritmo, tuple(sorted(mapa.bssids_generacion))) for mapa in mapas
    } == {
        (algoritmo, combo)
        for algoritmo in ("IDW",)
        for combo in {
            ("sp5:02:01:00:00",),
            ("sp5:02:02:00:00",),
            ("sp5:02:03:00:00",),
            ("sp5:02:01:00:00", "sp5:02:02:00:00", "sp5:02:03:00:00"),
        }
    }


def test_ubicacion_ap_conjunto_persiste_y_se_usa_en_heatmap(
    db_session,
    tecnico_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)
    conjunto = crear_conjunto_ap(
        plano_id=plano_id,
        body=ConjuntoAPCrearIn(
            nombre="AP puntual",
            proposito="Validar persistencia de ubicación.",
            banda_objetivo="2.4",
            bssids=["aa:bb:cc:dd:ee:01"],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )

    actualizado = actualizar_ubicacion_ap_conjunto(
        conjunto_id=conjunto.id,
        body=ActualizarUbicacionAPConjuntoIn(
            bssid="aa:bb:cc:dd:ee:01",
            pos_x=321,
            pos_y=123,
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )

    assert actualizado.items[0].pos_x == 321
    assert actualizado.items[0].pos_y == 123

    mapa = generar_heatmap_conjunto(
        conjunto_id=conjunto.id,
        body=GenerarHeatmapConjuntoIn(
            modo="INDIVIDUAL",
            bssids=["aa:bb:cc:dd:ee:01"],
            resolucion=64,
        ),
        request=None,
        db=db_session,
        current_user=tecnico_usuario,
    )

    assert mapa.ap_pos_x == 321
    assert mapa.ap_pos_y == 123


def test_conjunto_ap_persiste_potencia_tx_declarada(
    db_session,
    tecnico_usuario,
):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)

    conjunto = crear_conjunto_ap(
        plano_id=plano_id,
        body=ConjuntoAPCrearIn(
            nombre="AP con TX declarado",
            proposito="Registrar potencia declarada por el técnico.",
            banda_objetivo="2.4",
            bssids=["aa:bb:cc:dd:ee:01"],
            configuraciones_radio=[
                {
                    "bssid": "aa:bb:cc:dd:ee:01",
                    "potencia_tx_dbm": 12,
                    "fuente_potencia": "manual",
                    "confianza_potencia": "media",
                    "ganancia_dbi": 2.14,
                }
            ],
        ),
        db=db_session,
        current_user=tecnico_usuario,
    )

    item = conjunto.items[0]
    assert item.potencia_tx_dbm == 12
    assert item.fuente_potencia == "manual"
    assert item.confianza_potencia == "media"
    assert item.radios == [
        {
            "banda": "2.4",
            "potencia_dbm": 12.0,
            "fuente_potencia": "manual",
            "confianza_potencia": "media",
            "ganancia_dbi": 2.14,
        }
    ]


def test_conjunto_ap_rechaza_bssid_inexistente(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)

    with pytest.raises(HTTPException) as exc:
        crear_conjunto_ap(
            plano_id=plano_id,
            body=ConjuntoAPCrearIn(
                nombre="AP sospechoso",
                proposito="Validar una selección inválida.",
                bssids=["aa:bb:cc:dd:ee:99"],
            ),
            db=db_session,
            current_user=tecnico_usuario,
        )

    assert exc.value.status_code == 422
    assert "no existen en las mediciones" in exc.value.detail


def test_generar_heatmap_retorna_matriz_y_cache(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)

    mapa1 = generar_heatmap(
        plano_id=plano_id,
        request=None,
        bssid=["aa:bb:cc:dd:ee:01", "aa:bb:cc:dd:ee:02"],
        ap_pos_x=[210, 300],
        ap_pos_y=[140, 120],
        algoritmo="IDW",
        resolucion=64,
        db=db_session,
        current_user=tecnico_usuario,
    )
    mapa2 = generar_heatmap(
        plano_id=plano_id,
        request=None,
        bssid=["aa:bb:cc:dd:ee:01", "aa:bb:cc:dd:ee:02"],
        ap_pos_x=[210, 300],
        ap_pos_y=[140, 120],
        algoritmo="IDW",
        resolucion=64,
        db=db_session,
        current_user=tecnico_usuario,
    )

    assert mapa1.id == mapa2.id
    assert mapa1.bssid == "aa:bb:cc:dd:ee:01"
    assert mapa1.ssid == "BulldogCorp"
    assert mapa1.ap_pos_x == 210
    assert mapa1.ap_pos_y == 140
    assert [ap.bssid for ap in mapa1.aps_interes] == [
        "aa:bb:cc:dd:ee:01",
        "aa:bb:cc:dd:ee:02",
    ]
    assert mapa1.aps_interes[1].pos_x == 300
    assert mapa1.aps_interes[1].pos_y == 120
    assert mapa1.resolucion == 64
    assert len(mapa1.matriz) == 64
    assert len(mapa1.matriz[0]) == 64
    assert mapa1.url_imagen.startswith("/mapas/archivo/")
    assert mapa1.cantidad_puntos == 5
    assert len(mapa1.puntos_lectura) == 5
    assert mapa1.rssi_promedio == pytest.approx(
        sum(punto.rssi for punto in mapa1.puntos_lectura) / 5,
        abs=0.01,
    )
    assert mapa1.advertencias
    fila_lectura_fuerte = int((20 / 300) * 64)
    col_lectura_fuerte = int((20 / 400) * 64)
    assert mapa1.matriz[fila_lectura_fuerte][col_lectura_fuerte] >= -55
    fila_lectura_media = int((20 / 300) * 64)
    col_lectura_media = int((380 / 400) * 64)
    assert mapa1.matriz[fila_lectura_media][col_lectura_media] >= -65

    aps_recargados = listar_aps_disponibles(
        plano_id=plano_id,
        db=db_session,
        current_user=tecnico_usuario,
    )
    posiciones = {ap.bssid: (ap.pos_x, ap.pos_y) for ap in aps_recargados}
    seleccionados = {ap.bssid for ap in aps_recargados if ap.seleccionado}
    assert posiciones["aa:bb:cc:dd:ee:01"] == (210, 140)
    assert posiciones["aa:bb:cc:dd:ee:02"] == (300, 120)
    assert seleccionados == {"aa:bb:cc:dd:ee:01", "aa:bb:cc:dd:ee:02"}

    generar_heatmap(
        plano_id=plano_id,
        request=None,
        bssid=["aa:bb:cc:dd:ee:01"],
        ap_pos_x=[211],
        ap_pos_y=[141],
        algoritmo="IDW",
        resolucion=64,
        db=db_session,
        current_user=tecnico_usuario,
    )
    aps_tras_mapa_individual = listar_aps_disponibles(
        plano_id=plano_id,
        db=db_session,
        current_user=tecnico_usuario,
    )
    posiciones = {ap.bssid: (ap.pos_x, ap.pos_y) for ap in aps_tras_mapa_individual}
    seleccionados = {ap.bssid for ap in aps_tras_mapa_individual if ap.seleccionado}
    assert posiciones["aa:bb:cc:dd:ee:01"] == (211, 141)
    assert posiciones["aa:bb:cc:dd:ee:02"] == (300, 120)
    assert seleccionados == {"aa:bb:cc:dd:ee:01"}


def test_escala_heatmap_prioriza_umbral_operativo():
    etiquetas = [item["etiqueta"] for item in ESCALA_CWNA]
    assert etiquetas == [
        "Óptimo",
        "Aceptable",
        "Pobre",
        "Muy pobre",
        "Zona muerta",
    ]
    assert ESCALA_CWNA[0]["desde"] == -70
    assert ESCALA_CWNA[-1]["desde"] == -120


def test_render_heatmap_muestra_advertencia_en_menos_72_dbm():
    service = HeatmapImageService()

    assert service._color_para_rssi(-70) == (167, 232, 74)
    assert service._color_para_rssi(-72) == (241, 230, 74)
    assert service._color_para_rssi(-82) == (199, 184, 75)
    assert service._color_para_rssi(-86) == (126, 129, 115)
    assert service._color_para_rssi(-91) == (28, 28, 28)


def test_interpolacion_exige_soporte_local_para_islas_optimistas():
    service = InterpolacionService()
    matriz = service.interpolar(
        puntos=[
            PuntoRSSI(punto_id=1, x=200, y=150, rssi=-68),
            PuntoRSSI(punto_id=2, x=80, y=150, rssi=-95),
            PuntoRSSI(punto_id=3, x=320, y=150, rssi=-95),
            PuntoRSSI(punto_id=4, x=200, y=40, rssi=-95),
            PuntoRSSI(punto_id=5, x=200, y=260, rssi=-95),
        ],
        ancho_px=400,
        alto_px=300,
        resolucion=8,
        algoritmo="IDW",
    )

    valores_verdes = sum(1 for fila in matriz for valor in fila if valor >= -70)
    assert valores_verdes <= 2


def test_generar_heatmap_compone_mejor_rssi_por_punto(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    repo = MedicionRepository(db_session)
    lecturas = [
        (70, 80, -52, -92),
        (100, 80, -55, -90),
        (320, 220, -91, -53),
        (340, 230, -92, -56),
        (200, 150, -78, -78),
    ]
    for x, y, rssi_ap1, rssi_ap2 in lecturas:
        repo.crear_lote(
            plano_id=plano_id,
            pos_x=x,
            pos_y=y,
            items=[
                MedicionItemIn(
                    ssid="Quiroga",
                    bssid="aa:bb:cc:dd:ee:01",
                    rssi=rssi_ap1,
                    canal=6,
                    frecuencia_mhz=2437,
                ),
                MedicionItemIn(
                    ssid="Patas Sucias",
                    bssid="aa:bb:cc:dd:ee:02",
                    rssi=rssi_ap2,
                    canal=11,
                    frecuencia_mhz=2462,
                ),
            ],
        )

    mapa = generar_heatmap(
        plano_id=plano_id,
        request=None,
        bssid=["aa:bb:cc:dd:ee:01", "aa:bb:cc:dd:ee:02"],
        ap_pos_x=[380, 20],
        ap_pos_y=[20, 280],
        algoritmo="IDW",
        resolucion=64,
        db=db_session,
        current_user=tecnico_usuario,
    )

    fila_lectura_ap1 = int((80 / 300) * 64)
    col_lectura_ap1 = int((70 / 400) * 64)
    fila_lectura_ap2 = int((220 / 300) * 64)
    col_lectura_ap2 = int((320 / 400) * 64)
    fila_lectura_media = int((150 / 300) * 64)
    col_lectura_media = int((200 / 400) * 64)

    assert mapa.matriz[fila_lectura_ap1][col_lectura_ap1] >= -58
    assert mapa.matriz[fila_lectura_ap2][col_lectura_ap2] >= -58
    assert mapa.matriz[fila_lectura_media][col_lectura_media] <= -72

    mapa_posiciones_movidas = generar_heatmap(
        plano_id=plano_id,
        request=None,
        bssid=["aa:bb:cc:dd:ee:01", "aa:bb:cc:dd:ee:02"],
        ap_pos_x=[10, 390],
        ap_pos_y=[290, 10],
        algoritmo="IDW",
        resolucion=64,
        db=db_session,
        current_user=tecnico_usuario,
    )
    assert mapa_posiciones_movidas.matriz == mapa.matriz


def test_generar_heatmap_refleja_lecturas_asimetricas(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    repo = MedicionRepository(db_session)
    lecturas = [
        (280, 150, -52),
        (320, 150, -54),
        (120, 150, -88),
        (80, 150, -90),
        (200, 230, -76),
    ]
    for x, y, rssi in lecturas:
        repo.crear_lote(
            plano_id=plano_id,
            pos_x=x,
            pos_y=y,
            items=[
                MedicionItemIn(
                    ssid="Quiroga",
                    bssid="aa:bb:cc:dd:ee:01",
                    rssi=rssi,
                    canal=6,
                    frecuencia_mhz=2437,
                ),
            ],
        )

    mapa = generar_heatmap(
        plano_id=plano_id,
        request=None,
        bssid=["aa:bb:cc:dd:ee:01"],
        ap_pos_x=[200],
        ap_pos_y=[150],
        algoritmo="IDW",
        resolucion=64,
        db=db_session,
        current_user=tecnico_usuario,
    )

    fila = int((150 / 300) * 64)
    col_este = int((270 / 400) * 64)
    col_oeste = int((130 / 400) * 64)

    assert mapa.matriz[fila][col_este] >= -62
    assert mapa.matriz[fila][col_oeste] <= -78
    assert mapa.matriz[fila][col_este] - mapa.matriz[fila][col_oeste] >= 16


def test_resolver_aps_interes_rechaza_coordenadas_negativas():
    aps = [
        {
            "bssid": "aa:bb:cc:dd:ee:01",
            "ssid": "BulldogCorp",
            "canal": 6,
            "frecuencia_mhz": 2437,
            "rssi_promedio": -60,
            "pos_x": 10,
            "pos_y": 20,
            "cantidad_puntos": 5,
        }
    ]

    with pytest.raises(HTTPException) as exc:
        _resolver_aps_interes(
            aps=aps,
            bssids=["aa:bb:cc:dd:ee:01"],
            ap_pos_x=[-1],
            ap_pos_y=[20],
        )

    assert exc.value.status_code == 422
    assert "no pueden ser negativas" in exc.value.detail


def test_insertar_punto_invalida_cache_heatmap(db_session, tecnico_usuario):
    plano_id = _crear_plano_calibrado(db_session, tecnico_usuario)
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=5)

    mapa1 = generar_heatmap(
        plano_id=plano_id,
        request=None,
        bssid=["aa:bb:cc:dd:ee:01"],
        ap_pos_x=[210],
        ap_pos_y=[140],
        algoritmo="IDW",
        resolucion=64,
        db=db_session,
        current_user=tecnico_usuario,
    )
    _insertar_puntos_sinteticos(db_session, plano_id, cantidad=6)
    mapa2 = generar_heatmap(
        plano_id=plano_id,
        request=None,
        bssid=["aa:bb:cc:dd:ee:01"],
        ap_pos_x=[210],
        ap_pos_y=[140],
        algoritmo="IDW",
        resolucion=64,
        db=db_session,
        current_user=tecnico_usuario,
    )

    assert mapa2.id != mapa1.id


def test_interpolacion_200_puntos_resolucion_128_p95_menor_3s():
    puntos = [
        PuntoRSSI(
            punto_id=i + 1,
            x=(i % 20) * 20 + 5,
            y=(i // 20) * 30 + 5,
            rssi=float(-45 - (i % 55)),
        )
        for i in range(200)
    ]
    service = InterpolacionService()
    duraciones = []

    for _ in range(5):
        inicio = time.perf_counter()
        matriz = service.interpolar(
            puntos=puntos,
            ancho_px=400,
            alto_px=300,
            resolucion=128,
            algoritmo="IDW",
        )
        duraciones.append(time.perf_counter() - inicio)
        assert len(matriz) == 128
        assert len(matriz[0]) == 128

    p95_aproximado = sorted(duraciones)[-1]
    assert p95_aproximado <= 3.0


def test_interpolacion_rechaza_algoritmo_no_oficial():
    puntos = [
        PuntoRSSI(punto_id=1, x=40, y=40, rssi=-52),
        PuntoRSSI(punto_id=2, x=360, y=40, rssi=-82),
        PuntoRSSI(punto_id=3, x=40, y=260, rssi=-74),
        PuntoRSSI(punto_id=4, x=360, y=260, rssi=-58),
        PuntoRSSI(punto_id=5, x=200, y=150, rssi=-68),
    ]
    service = InterpolacionService()

    with pytest.raises(ValueError, match="Algoritmo no soportado"):
        service.interpolar(
            puntos=puntos,
            ancho_px=400,
            alto_px=300,
            resolucion=32,
            algoritmo="KRIGING",
        )
