# ruff: noqa: E501
"""Podar escenarios, reportes y diagnostico persistido.

Revision ID: 3c4d5e6f7a8b
Revises: 2b3c4d5e6f7a
Create Date: 2026-06-27
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "3c4d5e6f7a8b"
down_revision: str | None = "2b3c4d5e6f7a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    for tabla in (
        "reporte",
        "valor_proyectado_punto",
        "recomendacion_ap",
        "escenario_optimizado",
        "ap_detectado",
        "analisis_cobertura",
    ):
        op.drop_table(tabla)

    op.drop_index("ix_conjunto_ap_estado_gobernanza", table_name="conjunto_ap")
    op.drop_column("conjunto_ap", "estado_gobernanza")
    op.add_column("conjunto_ap", sa.Column("resumen_ia", sa.Text(), nullable=True))
    op.add_column("conjunto_ap", sa.Column("metricas_ia", sa.JSON(), nullable=True))
    op.add_column(
        "conjunto_ap",
        sa.Column("restricciones_ia", sa.JSON(), nullable=True),
    )
    op.add_column(
        "conjunto_ap",
        sa.Column("version_motor_ia", sa.String(length=30), nullable=True),
    )

    op.add_column(
        "conjunto_ap_item",
        sa.Column("accion_recomendada", sa.String(length=30), nullable=True),
    )
    op.add_column(
        "conjunto_ap_item", sa.Column("justificacion", sa.Text(), nullable=True)
    )
    op.add_column("conjunto_ap_item", sa.Column("altura_m", sa.Float(), nullable=True))
    op.add_column(
        "conjunto_ap_item",
        sa.Column("tipo_montaje", sa.String(length=30), nullable=True),
    )
    op.add_column(
        "conjunto_ap_item",
        sa.Column("banda", sa.String(length=10), nullable=True),
    )
    op.add_column(
        "conjunto_ap_item",
        sa.Column("modelo_ap", sa.String(length=120), nullable=True),
    )
    op.add_column(
        "conjunto_ap_item",
        sa.Column("costo_estimado", sa.Float(), nullable=True),
    )
    op.add_column("conjunto_ap_item", sa.Column("radios", sa.JSON(), nullable=True))


def downgrade() -> None:
    for columna in (
        "radios",
        "costo_estimado",
        "modelo_ap",
        "banda",
        "tipo_montaje",
        "altura_m",
        "justificacion",
        "accion_recomendada",
    ):
        op.drop_column("conjunto_ap_item", columna)

    for columna in (
        "version_motor_ia",
        "restricciones_ia",
        "metricas_ia",
        "resumen_ia",
    ):
        op.drop_column("conjunto_ap", columna)

    op.add_column(
        "conjunto_ap",
        sa.Column(
            "estado_gobernanza",
            sa.String(length=30),
            nullable=False,
            server_default="borrador_tecnico",
        ),
    )
    op.create_index(
        "ix_conjunto_ap_estado_gobernanza",
        "conjunto_ap",
        ["estado_gobernanza"],
    )

    op.create_table(
        "analisis_cobertura",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mapa_calor_id", sa.Integer(), nullable=False),
        sa.Column("pct_cobertura", sa.Float(), nullable=False),
        sa.Column("pct_zonas_muertas", sa.Float(), nullable=False),
        sa.Column("celdas_zonas_muertas", sa.Integer(), nullable=False),
        sa.Column("cantidad_solapamientos", sa.Integer(), nullable=False),
        sa.Column("cantidad_interferencias", sa.Integer(), nullable=False),
        sa.Column("hallazgos", sa.JSON(), nullable=False),
        sa.Column("resumen", sa.Text(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(
            ["mapa_calor_id"], ["mapa_calor.id"], ondelete="CASCADE"
        ),
        sa.UniqueConstraint("mapa_calor_id"),
    )
    op.create_table(
        "ap_detectado",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("analisis_id", sa.Integer(), nullable=False),
        sa.Column("bssid", sa.String(length=17), nullable=False),
        sa.Column("ssid", sa.String(length=255), nullable=False),
        sa.Column("canal", sa.Integer(), nullable=True),
        sa.Column("frecuencia_mhz", sa.Integer(), nullable=True),
        sa.Column("rssi_promedio", sa.Float(), nullable=False),
        sa.Column("pos_x", sa.Float(), nullable=False),
        sa.Column("pos_y", sa.Float(), nullable=False),
        sa.Column(
            "confirmado", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(
            ["analisis_id"], ["analisis_cobertura.id"], ondelete="CASCADE"
        ),
    )
    op.create_table(
        "escenario_optimizado",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("proyecto_id", sa.Integer(), nullable=False),
        sa.Column("plano_id", sa.Integer(), nullable=False),
        sa.Column("mapa_actual_id", sa.Integer(), nullable=True),
        sa.Column("mapa_proyectado_id", sa.Integer(), nullable=True),
        sa.Column("conjunto_base_id", sa.Integer(), nullable=True),
        sa.Column("origen", sa.String(length=30), nullable=False, server_default="ia"),
        sa.Column("estado_gobernanza", sa.String(length=30), nullable=False),
        sa.Column("generado_por_id", sa.Integer(), nullable=True),
        sa.Column("aprobado_por_id", sa.Integer(), nullable=True),
        sa.Column("publicado_por_id", sa.Integer(), nullable=True),
        sa.Column("aprobado_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("publicado_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("tipo_negocio", sa.String(length=30), nullable=False),
        sa.Column("perfil", sa.String(length=40), nullable=False),
        sa.Column("politica_combinacion", sa.String(length=50), nullable=False),
        sa.Column("banda", sa.String(length=10), nullable=False),
        sa.Column("bandas", sa.JSON(), nullable=False),
        sa.Column("modelo_ap", sa.String(length=120), nullable=False),
        sa.Column("pct_cobertura_actual", sa.Float(), nullable=False),
        sa.Column("pct_cobertura", sa.Float(), nullable=False),
        sa.Column("costo_estimado", sa.Float(), nullable=False),
        sa.Column("cantidad_aps", sa.Integer(), nullable=False),
        sa.Column("resumen", sa.Text(), nullable=False),
        sa.Column("restricciones", sa.JSON(), nullable=False),
        sa.Column("metricas", sa.JSON(), nullable=False),
        sa.Column("mapas_por_banda", sa.JSON(), nullable=False),
        sa.Column("mapas_actuales_por_banda", sa.JSON(), nullable=False),
        sa.Column("supuestos", sa.JSON(), nullable=False),
        sa.Column("confianza", sa.String(length=15), nullable=False),
        sa.Column("version_motor", sa.String(length=30), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(["proyecto_id"], ["proyecto.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plano_id"], ["plano.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["mapa_actual_id"], ["mapa_calor.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["mapa_proyectado_id"], ["mapa_calor.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["conjunto_base_id"], ["conjunto_ap.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["generado_por_id"], ["usuario.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["aprobado_por_id"], ["usuario.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["publicado_por_id"], ["usuario.id"], ondelete="SET NULL"
        ),
    )
    op.create_table(
        "recomendacion_ap",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("escenario_id", sa.Integer(), nullable=False),
        sa.Column("orden", sa.Integer(), nullable=False),
        sa.Column("ap_fisico_id", sa.Integer(), nullable=True),
        sa.Column("accion", sa.String(length=30), nullable=False),
        sa.Column("coord_x", sa.Float(), nullable=False),
        sa.Column("coord_y", sa.Float(), nullable=False),
        sa.Column("altura_m", sa.Float(), nullable=False),
        sa.Column("tipo_montaje", sa.String(length=30), nullable=False),
        sa.Column("banda", sa.String(length=10), nullable=False),
        sa.Column("modelo_ap", sa.String(length=120), nullable=False),
        sa.Column("costo_estimado", sa.Float(), nullable=False),
        sa.Column("rssi_proyectado", sa.Float(), nullable=False),
        sa.Column("radios", sa.JSON(), nullable=False),
        sa.Column("justificacion", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["escenario_id"], ["escenario_optimizado.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["ap_fisico_id"], ["ap_fisico.id"], ondelete="SET NULL"
        ),
    )
    op.create_table(
        "valor_proyectado_punto",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("escenario_id", sa.Integer(), nullable=False),
        sa.Column("punto_medicion_id", sa.Integer(), nullable=False),
        sa.Column("banda", sa.String(length=10), nullable=False),
        sa.Column("rssi_observado_dbm", sa.Float(), nullable=True),
        sa.Column("rssi_proyectado_dbm", sa.Float(), nullable=False),
        sa.Column("diferencia_db", sa.Float(), nullable=True),
        sa.Column("radio_primaria", sa.String(length=80), nullable=False),
        sa.Column("radio_secundaria", sa.String(length=80), nullable=True),
        sa.Column("rssi_secundario_dbm", sa.Float(), nullable=True),
        sa.Column("snr_proyectado_db", sa.Float(), nullable=True),
        sa.Column("incertidumbre_db", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["escenario_id"], ["escenario_optimizado.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["punto_medicion_id"], ["punto_medicion.id"], ondelete="CASCADE"
        ),
        sa.UniqueConstraint(
            "escenario_id",
            "punto_medicion_id",
            "banda",
            name="uq_valor_proyectado_escenario_punto_banda",
        ),
    )
    op.create_table(
        "reporte",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("proyecto_id", sa.Integer(), nullable=False),
        sa.Column("escenario_id", sa.Integer(), nullable=True),
        sa.Column("estado", sa.String(length=20), nullable=False),
        sa.Column("ruta_pdf", sa.String(length=500), nullable=True, unique=True),
        sa.Column("sha256", sa.String(length=64), nullable=True),
        sa.Column("tamanio_bytes", sa.Integer(), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(["proyecto_id"], ["proyecto.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["escenario_id"], ["escenario_optimizado.id"], ondelete="SET NULL"
        ),
    )
