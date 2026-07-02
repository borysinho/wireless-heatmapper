"""Repositorios del módulo de heatmap y conjuntos AP.

Sprint 4 — PB-05.
"""

from sqlalchemy.orm import Session

from app.models.heatmap import ConjuntoAP, ConjuntoAPItem, MapaCalor
from app.models.medicion import LecturaRSSI


class MapaCalorRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def obtener_por_id(self, *, mapa_id: int) -> MapaCalor | None:
        return self._db.query(MapaCalor).filter(MapaCalor.id == mapa_id).first()

    def obtener_por_ruta(self, *, ruta_imagen: str) -> MapaCalor | None:
        return (
            self._db.query(MapaCalor)
            .filter(MapaCalor.ruta_imagen == ruta_imagen)
            .first()
        )

    def obtener_cache(
        self,
        *,
        plano_id: int,
        algoritmo: str,
        resolucion: int,
        firma_mediciones: str,
    ) -> MapaCalor | None:
        return (
            self._db.query(MapaCalor)
            .filter(
                MapaCalor.plano_id == plano_id,
                MapaCalor.algoritmo == algoritmo,
                MapaCalor.resolucion == resolucion,
                MapaCalor.firma_mediciones == firma_mediciones,
            )
            .order_by(MapaCalor.created_at.desc(), MapaCalor.id.desc())
            .first()
        )

    def listar_recientes_por_plano(self, *, plano_id: int) -> list[MapaCalor]:
        return (
            self._db.query(MapaCalor)
            .filter(MapaCalor.plano_id == plano_id)
            .order_by(MapaCalor.created_at.desc(), MapaCalor.id.desc())
            .all()
        )

    def listar_por_clave_conjunto(
        self,
        *,
        conjunto_ap_id: int,
        modo_generacion: str,
        algoritmo: str,
        bssids: list[str],
    ) -> list[MapaCalor]:
        clave_bssids = tuple(sorted(bssid.lower() for bssid in bssids))
        candidatos = (
            self._db.query(MapaCalor)
            .filter(
                MapaCalor.conjunto_ap_id == conjunto_ap_id,
                MapaCalor.modo_generacion == modo_generacion,
                MapaCalor.algoritmo == algoritmo,
            )
            .order_by(MapaCalor.created_at.desc(), MapaCalor.id.desc())
            .all()
        )
        return [
            mapa
            for mapa in candidatos
            if tuple(
                sorted(
                    bssid.lower()
                    for bssid in (mapa.bssids_generacion or [mapa.bssid])
                )
            )
            == clave_bssids
        ]

    def crear(
        self,
        *,
        plano_id: int,
        conjunto_ap_id: int | None = None,
        modo_generacion: str = "SUBCONJUNTO",
        algoritmo: str,
        resolucion: int,
        bssid: str,
        ssid: str,
        ap_pos_x: float,
        ap_pos_y: float,
        aps_interes: list[dict],
        bssids_generacion: list[str] | None = None,
        matriz: list[list[float]],
        escala: list[dict],
        ruta_imagen: str,
        cantidad_puntos: int,
        rssi_min: float,
        rssi_max: float,
        firma_mediciones: str,
    ) -> MapaCalor:
        mapa = MapaCalor(
            plano_id=plano_id,
            conjunto_ap_id=conjunto_ap_id,
            modo_generacion=modo_generacion,
            algoritmo=algoritmo,
            resolucion=resolucion,
            bssid=bssid,
            ssid=ssid,
            ap_pos_x=ap_pos_x,
            ap_pos_y=ap_pos_y,
            aps_interes=aps_interes,
            bssids_generacion=bssids_generacion or [ap["bssid"] for ap in aps_interes],
            matriz=matriz,
            escala=escala,
            ruta_imagen=ruta_imagen,
            cantidad_puntos=cantidad_puntos,
            rssi_min=rssi_min,
            rssi_max=rssi_max,
            firma_mediciones=firma_mediciones,
        )
        self._db.add(mapa)
        self._db.commit()
        self._db.refresh(mapa)
        return mapa

    def actualizar_resultado(
        self,
        *,
        mapa: MapaCalor,
        modo_generacion: str,
        algoritmo: str,
        resolucion: int,
        bssid: str,
        ssid: str,
        ap_pos_x: float,
        ap_pos_y: float,
        aps_interes: list[dict],
        bssids_generacion: list[str],
        matriz: list[list[float]],
        escala: list[dict],
        ruta_imagen: str,
        cantidad_puntos: int,
        rssi_min: float,
        rssi_max: float,
        firma_mediciones: str,
    ) -> MapaCalor:
        mapa.modo_generacion = modo_generacion
        mapa.algoritmo = algoritmo
        mapa.resolucion = resolucion
        mapa.bssid = bssid
        mapa.ssid = ssid
        mapa.ap_pos_x = ap_pos_x
        mapa.ap_pos_y = ap_pos_y
        mapa.aps_interes = aps_interes
        mapa.bssids_generacion = bssids_generacion
        mapa.matriz = matriz
        mapa.escala = escala
        mapa.ruta_imagen = ruta_imagen
        mapa.cantidad_puntos = cantidad_puntos
        mapa.rssi_min = rssi_min
        mapa.rssi_max = rssi_max
        mapa.firma_mediciones = firma_mediciones
        self._db.commit()
        self._db.refresh(mapa)
        return mapa

    def invalidar_plano(self, *, plano_id: int) -> None:
        """Elimina resultados dependientes cuando cambian las mediciones del plano."""
        conjuntos_ia = (
            self._db.query(ConjuntoAP)
            .filter(
                ConjuntoAP.plano_id == plano_id,
                ConjuntoAP.origen == "ia",
            )
            .all()
        )
        (
            self._db.query(MapaCalor)
            .filter(MapaCalor.plano_id == plano_id)
            .delete(synchronize_session=False)
        )
        for conjunto in conjuntos_ia:
            (
                self._db.query(LecturaRSSI)
                .filter(LecturaRSSI.conjunto_ap_id == conjunto.id)
                .delete(synchronize_session=False)
            )
            self._db.delete(conjunto)

        self._db.flush()

    def eliminar(self, *, mapa: MapaCalor) -> None:
        self._db.delete(mapa)
        self._db.commit()


class ConjuntoAPRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def listar_por_plano(self, *, plano_id: int) -> list[ConjuntoAP]:
        return (
            self._db.query(ConjuntoAP)
            .filter(ConjuntoAP.plano_id == plano_id)
            .order_by(ConjuntoAP.updated_at.desc(), ConjuntoAP.id.desc())
            .all()
        )

    def obtener_por_id(self, *, conjunto_id: int) -> ConjuntoAP | None:
        return self._db.query(ConjuntoAP).filter(ConjuntoAP.id == conjunto_id).first()

    def existe_nombre(
        self,
        *,
        plano_id: int,
        nombre: str,
        excluir_id: int | None = None,
    ) -> bool:
        query = self._db.query(ConjuntoAP).filter(
            ConjuntoAP.plano_id == plano_id,
            ConjuntoAP.nombre == nombre,
        )
        if excluir_id is not None:
            query = query.filter(ConjuntoAP.id != excluir_id)
        return self._db.query(query.exists()).scalar() is True

    def crear(
        self,
        *,
        plano_id: int,
        nombre: str,
        proposito: str,
        descripcion: str | None,
        es_principal: bool,
        banda_objetivo: str = "5",
        items: list[dict],
        origen: str = "manual_movil",
        creado_por_id: int | None = None,
        conjunto_origen_id: int | None = None,
        resumen_ia: str | None = None,
        metricas_ia: dict | None = None,
        restricciones_ia: dict | None = None,
        version_motor_ia: str | None = None,
    ) -> ConjuntoAP:
        conjunto = ConjuntoAP(
            plano_id=plano_id,
            conjunto_origen_id=conjunto_origen_id,
            nombre=nombre,
            proposito=proposito,
            descripcion=descripcion,
            es_principal=es_principal,
            banda_objetivo=banda_objetivo,
            origen=origen,
            creado_por_id=creado_por_id,
            resumen_ia=resumen_ia,
            metricas_ia=metricas_ia,
            restricciones_ia=restricciones_ia,
            version_motor_ia=version_motor_ia,
        )
        self._db.add(conjunto)
        self._db.flush()
        self._reemplazar_items(conjunto=conjunto, items=items)
        self._db.commit()
        self._db.refresh(conjunto)
        return conjunto

    def actualizar(
        self,
        *,
        conjunto: ConjuntoAP,
        nombre: str | None = None,
        proposito: str | None = None,
        descripcion: str | None = None,
        es_principal: bool | None = None,
        banda_objetivo: str | None = None,
        items: list[dict] | None = None,
    ) -> ConjuntoAP:
        if nombre is not None:
            conjunto.nombre = nombre
        if proposito is not None:
            conjunto.proposito = proposito
        if descripcion is not None:
            conjunto.descripcion = descripcion
        if es_principal is not None:
            conjunto.es_principal = es_principal
        if banda_objetivo is not None:
            conjunto.banda_objetivo = banda_objetivo
        if items is not None:
            self._reemplazar_items(conjunto=conjunto, items=items)
        self._db.commit()
        self._db.refresh(conjunto)
        return conjunto

    def eliminar(self, *, conjunto: ConjuntoAP) -> None:
        (
            self._db.query(LecturaRSSI)
            .filter(LecturaRSSI.conjunto_ap_id == conjunto.id)
            .delete(synchronize_session=False)
        )
        for mapa in list(conjunto.mapas_calor):
            self._db.delete(mapa)
        self._db.delete(conjunto)
        self._db.commit()

    def actualizar_ubicacion_ap(
        self,
        *,
        conjunto: ConjuntoAP,
        bssid: str,
        pos_x: float,
        pos_y: float,
    ) -> ConjuntoAP | None:
        item = next(
            (item for item in conjunto.items if item.bssid.lower() == bssid.lower()),
            None,
        )
        if item is None:
            return None
        item.pos_x = pos_x
        item.pos_y = pos_y
        self._db.commit()
        self._db.refresh(conjunto)
        return conjunto

    def _reemplazar_items(self, *, conjunto: ConjuntoAP, items: list[dict]) -> None:
        conjunto.items.clear()
        self._db.flush()
        for item in items:
            conjunto.items.append(ConjuntoAPItem(**item))
