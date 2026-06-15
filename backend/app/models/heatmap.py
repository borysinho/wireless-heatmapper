"""Modelos ORM del módulo de heatmap y análisis.

Sprint 4 — PB-05 (Generar mapa de calor), PB-06 (Analizar cobertura).
"""

import sqlalchemy as sa
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class MapaCalor(Base):
    """Resultado de interpolación generado desde las mediciones de un plano."""

    __tablename__ = "mapa_calor"

    id = Column(Integer, primary_key=True, index=True)
    plano_id = Column(
        Integer,
        ForeignKey("plano.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    algoritmo = Column(String(20), nullable=False, default="IDW")
    resolucion = Column(Integer, nullable=False, default=128)
    matriz = Column(sa.JSON().with_variant(sa.JSON, "sqlite"), nullable=False)
    escala = Column(sa.JSON().with_variant(sa.JSON, "sqlite"), nullable=False)
    ruta_imagen = Column(String(500), nullable=False, unique=True)
    cantidad_puntos = Column(Integer, nullable=False)
    rssi_min = Column(Float, nullable=False)
    rssi_max = Column(Float, nullable=False)
    firma_mediciones = Column(String(120), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plano = relationship("Plano", back_populates="mapas_calor")
    analisis = relationship(
        "AnalisisCobertura",
        back_populates="mapa",
        cascade="all, delete-orphan",
        uselist=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "plano_id",
            "algoritmo",
            "resolucion",
            "firma_mediciones",
            name="uq_mapa_calor_cache",
        ),
        {"sqlite_autoincrement": True},
    )


class AnalisisCobertura(Base):
    """Diagnóstico automático generado a partir de un mapa de calor."""

    __tablename__ = "analisis_cobertura"

    id = Column(Integer, primary_key=True, index=True)
    mapa_calor_id = Column(
        Integer,
        ForeignKey("mapa_calor.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    pct_cobertura = Column(Float, nullable=False)
    pct_zonas_muertas = Column(Float, nullable=False)
    celdas_zonas_muertas = Column(Integer, nullable=False)
    cantidad_solapamientos = Column(Integer, nullable=False)
    cantidad_interferencias = Column(Integer, nullable=False)
    hallazgos = Column(sa.JSON().with_variant(sa.JSON, "sqlite"), nullable=False)
    resumen = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    mapa = relationship("MapaCalor", back_populates="analisis")
    aps_detectados = relationship(
        "APDetectado",
        back_populates="analisis",
        cascade="all, delete-orphan",
        order_by="APDetectado.rssi_promedio.desc()",
    )


class APDetectado(Base):
    """Access point detectado durante el relevamiento de un plano."""

    __tablename__ = "ap_detectado"

    id = Column(Integer, primary_key=True, index=True)
    analisis_id = Column(
        Integer,
        ForeignKey("analisis_cobertura.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    bssid = Column(String(17), nullable=False)
    ssid = Column(String(255), nullable=False)
    canal = Column(Integer, nullable=True)
    frecuencia_mhz = Column(Integer, nullable=True)
    rssi_promedio = Column(Float, nullable=False)
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    confirmado = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analisis = relationship("AnalisisCobertura", back_populates="aps_detectados")
