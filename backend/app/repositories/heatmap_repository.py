"""Repositorios del módulo de heatmap y análisis.

Sprint 4 — PB-05, PB-06.
"""

from sqlalchemy.orm import Session

from app.models.heatmap import AnalisisCobertura, APDetectado, MapaCalor


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
            .order_by(MapaCalor.created_at.desc())
            .first()
        )

    def crear(
        self,
        *,
        plano_id: int,
        algoritmo: str,
        resolucion: int,
        bssid: str,
        ssid: str,
        ap_pos_x: float,
        ap_pos_y: float,
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
            algoritmo=algoritmo,
            resolucion=resolucion,
            bssid=bssid,
            ssid=ssid,
            ap_pos_x=ap_pos_x,
            ap_pos_y=ap_pos_y,
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

    def invalidar_plano(self, *, plano_id: int) -> None:
        """Elimina mapas cacheados de un plano cuando cambian sus mediciones."""
        (
            self._db.query(MapaCalor)
            .filter(MapaCalor.plano_id == plano_id)
            .delete(synchronize_session=False)
        )


class AnalisisCoberturaRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def obtener_ap_por_id(self, *, ap_id: int) -> APDetectado | None:
        return self._db.query(APDetectado).filter(APDetectado.id == ap_id).first()

    def reemplazar(
        self,
        *,
        mapa: MapaCalor,
        pct_cobertura: float,
        pct_zonas_muertas: float,
        celdas_zonas_muertas: int,
        cantidad_solapamientos: int,
        cantidad_interferencias: int,
        hallazgos: dict,
        resumen: str,
        aps_detectados: list[dict],
    ) -> AnalisisCobertura:
        if mapa.analisis is not None:
            self._db.delete(mapa.analisis)
            self._db.flush()

        analisis = AnalisisCobertura(
            mapa_calor_id=mapa.id,
            pct_cobertura=pct_cobertura,
            pct_zonas_muertas=pct_zonas_muertas,
            celdas_zonas_muertas=celdas_zonas_muertas,
            cantidad_solapamientos=cantidad_solapamientos,
            cantidad_interferencias=cantidad_interferencias,
            hallazgos=hallazgos,
            resumen=resumen,
        )
        self._db.add(analisis)
        self._db.flush()

        for ap_data in aps_detectados:
            self._db.add(APDetectado(analisis_id=analisis.id, **ap_data))

        self._db.commit()
        self._db.refresh(analisis)
        return analisis

    def confirmar_ap(
        self,
        *,
        ap: APDetectado,
        pos_x: float,
        pos_y: float,
        confirmado: bool,
    ) -> APDetectado:
        ap.pos_x = pos_x
        ap.pos_y = pos_y
        ap.confirmado = confirmado
        self._db.commit()
        self._db.refresh(ap)
        return ap
