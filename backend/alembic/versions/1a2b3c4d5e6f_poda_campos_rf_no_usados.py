"""Poda de campos RF no usados en survey ni optimizacion.

Revision ID: 1a2b3c4d5e6f
Revises: 0a1b2c3d4e5f
Create Date: 2026-06-27
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "1a2b3c4d5e6f"
down_revision: str | None = "0a1b2c3d4e5f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index(
        "ix_medicion_wifi_instantanea_rf_id",
        table_name="medicion_wifi",
    )
    op.drop_constraint(
        "fk_medicion_wifi_instantanea_rf",
        "medicion_wifi",
        type_="foreignkey",
    )
    op.drop_column("medicion_wifi", "instantanea_rf_id")
    op.drop_table("instantanea_configuracion_rf")

    op.drop_column("ap_fisico", "costo_referencial")
    op.drop_column("ap_fisico", "procedencia")

    for columna in (
        "potencia_original",
        "unidad_potencia_original",
        "modo_gestion_rf",
        "dfs_permitido",
        "dominio_regulatorio",
        "modelo_antena",
        "beamwidth_horizontal",
        "beamwidth_vertical",
        "azimut_grados",
        "inclinacion_grados",
        "procedencia",
    ):
        op.drop_column("radio_ap", columna)

    op.drop_column("bssid_radio", "observado")
    op.drop_column("bssid_radio", "procedencia")


def downgrade() -> None:
    op.add_column(
        "bssid_radio",
        sa.Column(
            "procedencia",
            sa.String(length=30),
            nullable=False,
            server_default="DETECTADA_ANDROID",
        ),
    )
    op.add_column(
        "bssid_radio",
        sa.Column("observado", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    columnas_radio = (
        (
            "procedencia",
            sa.String(length=30),
            "INGRESADA_TECNICO",
        ),
        ("inclinacion_grados", sa.Float(), "0.0"),
        ("azimut_grados", sa.Float(), "0.0"),
        ("beamwidth_vertical", sa.Float(), "60.0"),
        ("beamwidth_horizontal", sa.Float(), "360.0"),
        ("modelo_antena", sa.String(length=120), None),
        ("dominio_regulatorio", sa.String(length=10), "BO"),
        ("dfs_permitido", sa.Boolean(), sa.false()),
        ("modo_gestion_rf", sa.String(length=15), "ESTATICO"),
        ("unidad_potencia_original", sa.String(length=10), "DBM"),
        ("potencia_original", sa.Float(), "0"),
    )
    for nombre, tipo, defecto in columnas_radio:
        op.add_column(
            "radio_ap",
            sa.Column(
                nombre,
                tipo,
                nullable=defecto is None,
                server_default=defecto,
            ),
        )

    op.add_column(
        "ap_fisico",
        sa.Column(
            "procedencia",
            sa.String(length=30),
            nullable=False,
            server_default="INGRESADA_TECNICO",
        ),
    )
    op.add_column(
        "ap_fisico",
        sa.Column("costo_referencial", sa.Float(), nullable=True),
    )

    op.create_table(
        "instantanea_configuracion_rf",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("radio_id", sa.Integer(), nullable=True),
        sa.Column("datos", sa.JSON(), nullable=False),
        sa.Column("procedencia", sa.String(30), nullable=False),
        sa.Column("completitud", sa.Float(), nullable=False),
        sa.Column(
            "capturada_en",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(["radio_id"], ["radio_ap.id"], ondelete="SET NULL"),
    )
    op.add_column(
        "medicion_wifi",
        sa.Column("instantanea_rf_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_medicion_wifi_instantanea_rf",
        "medicion_wifi",
        "instantanea_configuracion_rf",
        ["instantanea_rf_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "ix_medicion_wifi_instantanea_rf_id",
        "medicion_wifi",
        ["instantanea_rf_id"],
    )
