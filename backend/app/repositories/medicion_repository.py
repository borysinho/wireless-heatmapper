"""Repositorio de acceso a datos para lecturas RSSI.

Sprint 3 — PB-03 (Captura WiFi en línea), PB-04 (Marcar puntos de medición).
"""

from collections import Counter, defaultdict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.medicion import LecturaRSSI, PuntoMedicion, clasificar_nivel
from app.schemas.medicion import MedicionItemIn
from app.services.interpolacion_service import PuntoRSSI

RSSI_NO_DETECTADO_DBM = -95.0
ORIGEN_CAMPO = "CAMPO"
ORIGEN_IA_ESTIMADA = "IA_ESTIMADA"


class MedicionRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    # ------------------------------------------------------------------
    # Escritura — PB-03 (POST /api/mediciones)
    # ------------------------------------------------------------------

    def crear_lote(
        self,
        *,
        plano_id: int,
        pos_x: float,
        pos_y: float,
        items: list[MedicionItemIn],
    ) -> PuntoMedicion:
        """Persiste el lote completo en una sola transacción.

        1. Calcula el ``nivel`` de cada medición individual.
        2. Determina el peor nivel del lote (el del punto).
        3. Inserta ``punto_medicion`` + N filas ``lectura_rssi`` de campo.
        """
        # Clasificar individualmente cada ítem
        niveles_rssi = [clasificar_nivel(item.rssi) for item in items]
        _ORDEN = {"verde": 0, "amarillo": 1, "naranja": 2, "rojo": 3, "negro": 4}
        nivel_punto = max(niveles_rssi, key=lambda n: _ORDEN[n])

        punto = PuntoMedicion(
            plano_id=plano_id,
            pos_x=pos_x,
            pos_y=pos_y,
            nivel=nivel_punto,
        )
        self._db.add(punto)
        self._db.flush()  # obtiene punto.id sin cerrar la transacción

        for item, nivel_item in zip(items, niveles_rssi):
            lectura = LecturaRSSI(
                punto_id=punto.id,
                ssid=item.ssid,
                bssid=item.bssid.lower(),
                rssi=item.rssi,
                canal=item.canal,
                frecuencia_mhz=item.frecuencia_mhz,
                nivel=nivel_item,
                numero_lectura=1,
                origen=ORIGEN_CAMPO,
            )
            self._db.add(lectura)

        self._db.commit()
        self._db.refresh(punto)
        return punto

    # ------------------------------------------------------------------
    # Escritura — modo continuo (POST /api/puntos/{id}/mediciones)
    # ------------------------------------------------------------------

    def agregar_mediciones(
        self,
        *,
        punto: PuntoMedicion,
        items: list[MedicionItemIn],
    ) -> PuntoMedicion:
        """Agrega un nuevo lote de mediciones a un punto existente.

        Recalcula el ``nivel`` del punto tomando el peor RSSI
        de **todas** las mediciones acumuladas (anteriores + nuevas).
        El ``numero_lectura`` se incrementa respecto al lote anterior.
        """
        _ORDEN = {"verde": 0, "amarillo": 1, "naranja": 2, "rojo": 3, "negro": 4}

        # Determinar el siguiente número de lectura
        siguiente_lectura = (
            max((m.numero_lectura for m in punto.mediciones), default=0) + 1
        )

        for item in items:
            nivel_item = clasificar_nivel(item.rssi)
            lectura = LecturaRSSI(
                punto_id=punto.id,
                ssid=item.ssid,
                bssid=item.bssid.lower(),
                rssi=item.rssi,
                canal=item.canal,
                frecuencia_mhz=item.frecuencia_mhz,
                nivel=nivel_item,
                numero_lectura=siguiente_lectura,
                origen=ORIGEN_CAMPO,
            )
            self._db.add(lectura)

        self._db.flush()  # inserta las nuevas filas sin cerrar la transacción
        self._db.refresh(punto)  # recarga la relación mediciones

        todos_niveles = [m.nivel for m in punto.mediciones]
        punto.nivel = max(todos_niveles, key=lambda n: _ORDEN[n])

        self._db.commit()
        self._db.refresh(punto)
        return punto

    # ------------------------------------------------------------------
    # Lectura — PB-04 (GET /api/planos/{id}/puntos, GET /api/puntos/{id})
    # ------------------------------------------------------------------

    def listar_puntos_por_plano(self, *, plano_id: int) -> list[PuntoMedicion]:
        """Retorna todos los puntos de medición de un plano, más recientes primero."""
        return (
            self._db.query(PuntoMedicion)
            .filter(PuntoMedicion.plano_id == plano_id)
            .order_by(PuntoMedicion.created_at.desc())
            .all()
        )

    def listar_lecturas_por_plano(
        self,
        *,
        plano_id: int,
        origen: str = ORIGEN_CAMPO,
        conjunto_ap_id: int | None = None,
    ) -> list[LecturaRSSI]:
        """Retorna lecturas RSSI de todos los puntos del plano."""
        query = (
            self._db.query(LecturaRSSI)
            .join(PuntoMedicion, LecturaRSSI.punto_id == PuntoMedicion.id)
            .filter(PuntoMedicion.plano_id == plano_id)
            .filter(LecturaRSSI.origen == origen)
        )
        if conjunto_ap_id is not None:
            query = query.filter(LecturaRSSI.conjunto_ap_id == conjunto_ap_id)
        return query.order_by(LecturaRSSI.bssid.asc(), LecturaRSSI.rssi.desc()).all()

    def listar_mediciones_por_plano(self, *, plano_id: int) -> list[LecturaRSSI]:
        """Compatibilidad: retorna solo lecturas reales de campo."""
        return self.listar_lecturas_por_plano(plano_id=plano_id)

    def listar_aps_por_plano(
        self,
        *,
        plano_id: int,
        origen: str = ORIGEN_CAMPO,
        conjunto_ap_id: int | None = None,
    ) -> list[dict]:
        """Agrupa lecturas por BSSID para seleccionar APs de interés."""
        lecturas = self.listar_lecturas_por_plano(
            plano_id=plano_id,
            origen=origen,
            conjunto_ap_id=conjunto_ap_id,
        )
        por_bssid: dict[str, list[LecturaRSSI]] = defaultdict(list)
        for lectura in lecturas:
            por_bssid[lectura.bssid].append(lectura)

        aps: list[dict] = []
        for bssid, items in por_bssid.items():
            ssid = Counter(item.ssid for item in items).most_common(1)[0][0]
            canales = [item.canal for item in items if item.canal is not None]
            frecuencias = [
                item.frecuencia_mhz for item in items if item.frecuencia_mhz is not None
            ]
            peso_total = 0.0
            suma_x = 0.0
            suma_y = 0.0
            puntos_unicos = {item.punto_id for item in items}
            for item in items:
                peso = max(1.0, item.rssi + 120.0)
                peso_total += peso
                suma_x += item.punto.pos_x * peso
                suma_y += item.punto.pos_y * peso

            aps.append(
                {
                    "bssid": bssid,
                    "ssid": ssid,
                    "canal": Counter(canales).most_common(1)[0][0] if canales else None,
                    "frecuencia_mhz": Counter(frecuencias).most_common(1)[0][0]
                    if frecuencias
                    else None,
                    "rssi_promedio": round(
                        sum(item.rssi for item in items) / len(items),
                        2,
                    ),
                    "pos_x": round(suma_x / peso_total, 2),
                    "pos_y": round(suma_y / peso_total, 2),
                    "cantidad_puntos": len(puntos_unicos),
                }
            )
        return sorted(aps, key=lambda ap: ap["rssi_promedio"], reverse=True)

    def obtener_ap_por_bssid(self, *, plano_id: int, bssid: str) -> dict | None:
        bssid_norm = bssid.lower()
        for ap in self.listar_aps_por_plano(plano_id=plano_id):
            if ap["bssid"] == bssid_norm:
                return ap
        return None

    def listar_puntos_rssi_heatmap(
        self,
        *,
        plano_id: int,
        bssids: list[str],
        origen: str = ORIGEN_CAMPO,
        conjunto_ap_id: int | None = None,
    ) -> list[PuntoRSSI]:
        """Agrega cada punto al mejor RSSI de los APs de interés seleccionados.

        Si ningún AP seleccionado aparece en un punto de captura, se registra un
        piso de no-detección. Omitir esos puntos vuelve optimista el heatmap:
        elimina precisamente las zonas donde el cliente dejó de ver la red.
        """
        bssids_norm = {bssid.lower() for bssid in bssids}
        puntos = self.listar_puntos_por_plano(plano_id=plano_id)
        resultado: list[PuntoRSSI] = []
        for punto in puntos:
            rssi_por_bssid: dict[str, list[int]] = defaultdict(list)
            for lectura in punto.lecturas:
                if lectura.origen != origen:
                    continue
                if conjunto_ap_id is not None and lectura.conjunto_ap_id != conjunto_ap_id:
                    continue
                if lectura.bssid in bssids_norm:
                    rssi_por_bssid[lectura.bssid].append(lectura.rssi)
            mejor_rssi = (
                max(sum(valores) / len(valores) for valores in rssi_por_bssid.values())
                if rssi_por_bssid
                else RSSI_NO_DETECTADO_DBM
            )
            resultado.append(
                PuntoRSSI(
                    punto_id=punto.id,
                    x=punto.pos_x,
                    y=punto.pos_y,
                    rssi=float(mejor_rssi),
                )
            )
        return resultado

    def listar_puntos_rssi_por_bssid_heatmap(
        self,
        *,
        plano_id: int,
        bssids: list[str],
        origen: str = ORIGEN_CAMPO,
        conjunto_ap_id: int | None = None,
    ) -> dict[str, list[PuntoRSSI]]:
        """Agrupa lecturas RSSI por AP de interés y punto de medición."""
        bssids_norm = {bssid.lower() for bssid in bssids}
        puntos = self.listar_puntos_por_plano(plano_id=plano_id)
        resultado: dict[str, list[PuntoRSSI]] = {bssid: [] for bssid in bssids_norm}
        for punto in puntos:
            rssi_por_bssid: dict[str, list[int]] = defaultdict(list)
            for lectura in punto.lecturas:
                if lectura.origen != origen:
                    continue
                if conjunto_ap_id is not None and lectura.conjunto_ap_id != conjunto_ap_id:
                    continue
                if lectura.bssid in bssids_norm:
                    rssi_por_bssid[lectura.bssid].append(lectura.rssi)

            for bssid, valores in rssi_por_bssid.items():
                resultado[bssid].append(
                    PuntoRSSI(
                        punto_id=punto.id,
                        x=punto.pos_x,
                        y=punto.pos_y,
                        rssi=float(sum(valores) / len(valores)),
                    )
                )
        return resultado

    def rssi_maximo_por_bssid(
        self,
        *,
        plano_id: int,
        bssids: list[str],
    ) -> dict[str, float]:
        """Retorna el RSSI máximo observado para cada AP de interés."""
        filas = (
            self._db.query(LecturaRSSI.bssid, func.max(LecturaRSSI.rssi))
            .join(PuntoMedicion, LecturaRSSI.punto_id == PuntoMedicion.id)
            .filter(PuntoMedicion.plano_id == plano_id)
            .filter(LecturaRSSI.origen == ORIGEN_CAMPO)
            .filter(LecturaRSSI.bssid.in_([bssid.lower() for bssid in bssids]))
            .group_by(LecturaRSSI.bssid)
            .all()
        )
        return {bssid: float(rssi) for bssid, rssi in filas if rssi is not None}

    def firma_mediciones_plano(
        self,
        *,
        plano_id: int,
        bssids: list[str] | None = None,
        origen: str = ORIGEN_CAMPO,
        conjunto_ap_id: int | None = None,
    ) -> str:
        """Firma liviana del estado de lecturas usada para cache del heatmap."""
        query = (
            self._db.query(
                func.count(LecturaRSSI.id),
                func.max(PuntoMedicion.id),
                func.max(LecturaRSSI.id),
            )
            .join(PuntoMedicion, LecturaRSSI.punto_id == PuntoMedicion.id)
            .filter(PuntoMedicion.plano_id == plano_id)
            .filter(LecturaRSSI.origen == origen)
        )
        if conjunto_ap_id is not None:
            query = query.filter(LecturaRSSI.conjunto_ap_id == conjunto_ap_id)
        if bssids is not None:
            query = query.filter(
                LecturaRSSI.bssid.in_([bssid.lower() for bssid in bssids])
            )
        conteo, max_punto, max_lectura = query.one()
        return f"{origen}:{conjunto_ap_id or 0}:{conteo or 0}:{max_punto or 0}:{max_lectura or 0}"

    def reemplazar_lecturas_estimadas(
        self,
        *,
        conjunto_ap_id: int,
        lecturas: list[dict],
    ) -> None:
        """Reemplaza las lecturas IA de un conjunto derivado."""
        (
            self._db.query(LecturaRSSI)
            .filter(
                LecturaRSSI.origen == ORIGEN_IA_ESTIMADA,
                LecturaRSSI.conjunto_ap_id == conjunto_ap_id,
            )
            .delete(synchronize_session=False)
        )
        for item in lecturas:
            rssi = int(round(float(item["rssi"])))
            self._db.add(
                LecturaRSSI(
                    punto_id=int(item["punto_id"]),
                    ssid=str(item["ssid"]),
                    bssid=str(item["bssid"]).lower(),
                    rssi=max(-120, min(0, rssi)),
                    canal=item.get("canal"),
                    frecuencia_mhz=item.get("frecuencia_mhz"),
                    nivel=clasificar_nivel(max(-120, min(0, rssi))),
                    numero_lectura=1,
                    origen=ORIGEN_IA_ESTIMADA,
                    conjunto_ap_id=conjunto_ap_id,
                    modelo_origen=item.get("modelo_origen"),
                    incertidumbre_db=item.get("incertidumbre_db"),
                )
            )
        self._db.commit()

    def obtener_punto_por_id(self, *, punto_id: int) -> PuntoMedicion | None:
        """Retorna el punto con sus mediciones cargadas (eager via relationship)."""
        return (
            self._db.query(PuntoMedicion).filter(PuntoMedicion.id == punto_id).first()
        )

    def actualizar_posicion(
        self,
        *,
        punto: PuntoMedicion,
        pos_x: float,
        pos_y: float,
    ) -> PuntoMedicion:
        """Actualiza la posición de un punto sin alterar sus mediciones."""
        punto.pos_x = pos_x
        punto.pos_y = pos_y
        self._db.flush()
        return punto

    # ------------------------------------------------------------------
    # Eliminación — PB-04 (DELETE /api/puntos/{id})
    # ------------------------------------------------------------------

    def eliminar_punto(self, *, punto: PuntoMedicion) -> None:
        """Elimina el punto y sus mediciones en cascada."""
        self._db.delete(punto)
        self._db.commit()
