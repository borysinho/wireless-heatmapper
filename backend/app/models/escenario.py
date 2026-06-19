"""Modelos ORM de Sprint 5: IA, escenarios y reportes.

PB-07, PB-12 y PB-08 implementan optimización IA, comparación de escenarios
y reportes PDF persistidos en el backend.
"""

import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class EscenarioOptimizado(Base):
    """Alternativa de red propuesta por el optimizador de APs."""

    __tablename__ = "escenario_optimizado"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(
        Integer,
        ForeignKey("proyecto.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    plano_id = Column(
        Integer,
        ForeignKey("plano.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    mapa_actual_id = Column(
        Integer,
        ForeignKey("mapa_calor.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    mapa_proyectado_id = Column(
        Integer,
        ForeignKey("mapa_calor.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    nombre = Column(String(120), nullable=False)
    banda = Column(String(10), nullable=False, default="5")
    modelo_ap = Column(String(120), nullable=False)
    pct_cobertura_actual = Column(Float, nullable=False, default=0)
    pct_cobertura = Column(Float, nullable=False)
    costo_estimado = Column(Float, nullable=False, default=0)
    cantidad_aps = Column(Integer, nullable=False)
    resumen = Column(Text, nullable=False)
    restricciones = Column(sa.JSON().with_variant(sa.JSON, "sqlite"), nullable=False)
    metricas = Column(sa.JSON().with_variant(sa.JSON, "sqlite"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    proyecto = relationship("Proyecto", back_populates="escenarios")
    plano = relationship("Plano")
    mapa_actual = relationship("MapaCalor", foreign_keys=[mapa_actual_id])
    mapa_proyectado = relationship("MapaCalor", foreign_keys=[mapa_proyectado_id])
    recomendaciones = relationship(
        "RecomendacionAP",
        back_populates="escenario",
        cascade="all, delete-orphan",
        order_by="RecomendacionAP.orden.asc()",
    )


class RecomendacionAP(Base):
    """Acción sugerida sobre un AP para mejorar la cobertura."""

    __tablename__ = "recomendacion_ap"

    id = Column(Integer, primary_key=True, index=True)
    escenario_id = Column(
        Integer,
        ForeignKey("escenario_optimizado.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    orden = Column(Integer, nullable=False, default=1)
    accion = Column(String(30), nullable=False)
    coord_x = Column(Float, nullable=False)
    coord_y = Column(Float, nullable=False)
    banda = Column(String(10), nullable=False, default="5")
    modelo_ap = Column(String(120), nullable=False)
    costo_estimado = Column(Float, nullable=False, default=0)
    rssi_proyectado = Column(Float, nullable=False)
    justificacion = Column(Text, nullable=False)

    escenario = relationship("EscenarioOptimizado", back_populates="recomendaciones")


class Reporte(Base):
    """Reporte técnico PDF generado para un proyecto."""

    __tablename__ = "reporte"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(
        Integer,
        ForeignKey("proyecto.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    escenario_id = Column(
        Integer,
        ForeignKey("escenario_optimizado.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    estado = Column(String(20), nullable=False, default="LISTO")
    ruta_pdf = Column(String(500), nullable=True, unique=True)
    sha256 = Column(String(64), nullable=True)
    tamanio_bytes = Column(Integer, nullable=False, default=0)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    proyecto = relationship("Proyecto", back_populates="reportes")
    escenario = relationship("EscenarioOptimizado")
