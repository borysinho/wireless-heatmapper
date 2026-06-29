"""Modelos ORM para puntos de medición y lecturas RSSI.

Sprint 3 — PB-03 (Captura WiFi en línea), PB-04 (Marcar puntos de medición).

Tablas:
  - ``punto_medicion``: posición (píxeles del plano) con nivel agregado.
  - ``lectura_rssi``: una lectura RSSI real o estimada para un BSSID.

Clasificación CWNA-107 por RSSI (campo ``nivel``):
  verde    ≥ −70 dBm  → cobertura óptima
  amarillo −70..−80   → aceptable
  naranja  −80..−85   → pobre
  rojo     −85..−90   → muy pobre
  negro    < −90 dBm  → zona muerta
"""

import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base

nivel_senal_enum = sa.Enum(
    "verde",
    "amarillo",
    "naranja",
    "rojo",
    "negro",
    name="nivel_senal",
    create_type=False,
)


def clasificar_nivel(rssi: int) -> str:
    """Clasifica un valor RSSI según umbrales CWNA-107."""
    if rssi >= -70:
        return "verde"
    if rssi >= -80:
        return "amarillo"
    if rssi >= -85:
        return "naranja"
    if rssi >= -90:
        return "rojo"
    return "negro"


class PuntoMedicion(Base):
    """Punto de medición sobre el plano (posición en píxeles).

    El ``nivel`` refleja el peor RSSI (BSSID más débil) del lote capturado,
    calculado en el repositorio al insertar.
    """

    __tablename__ = "punto_medicion"

    id = Column(Integer, primary_key=True, index=True)
    plano_id = Column(
        Integer,
        ForeignKey("plano.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    nivel = Column(nivel_senal_enum, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plano = relationship("Plano", back_populates="puntos_medicion")
    lecturas = relationship(
        "LecturaRSSI",
        back_populates="punto",
        cascade="all, delete-orphan",
        order_by="[LecturaRSSI.numero_lectura.asc(), LecturaRSSI.rssi.desc()]",
    )

    @property
    def mediciones(self):
        """Compatibilidad de API: expone solo lecturas reales como ``mediciones``."""
        return [lectura for lectura in self.lecturas if lectura.origen == "CAMPO"]


class LecturaRSSI(Base):
    """Lectura RSSI real o estimada asociada a un punto del plano.

    ``bssid`` almacena la MAC normalizada en minúsculas (``aa:bb:cc:dd:ee:ff``).
    ``origen`` separa la evidencia de campo de valores estimados por IA.
    """

    __tablename__ = "lectura_rssi"

    id = Column(Integer, primary_key=True, index=True)
    punto_id = Column(
        Integer,
        ForeignKey("punto_medicion.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ssid = Column(String(255), nullable=False)
    bssid = Column(String(17), nullable=False)
    rssi = Column(Integer, nullable=False)
    canal = Column(Integer, nullable=True)
    frecuencia_mhz = Column(Integer, nullable=True)
    nivel = Column(nivel_senal_enum, nullable=False)
    numero_lectura = Column(Integer, nullable=False, default=1)
    origen = Column(String(20), nullable=False, default="CAMPO", index=True)
    conjunto_ap_id = Column(
        Integer,
        ForeignKey("conjunto_ap.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    mapa_calor_id = Column(
        Integer,
        ForeignKey("mapa_calor.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    modelo_origen = Column(String(60), nullable=True)
    incertidumbre_db = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    punto = relationship("PuntoMedicion", back_populates="lecturas")
