"""Lectura RSSI unificada y poda de inventario RF físico.

Revision ID: 5e6f7a8b9c0d
Revises: 4d5e6f7a8b9c
Create Date: 2026-06-28
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "5e6f7a8b9c0d"
down_revision: str | None = "4d5e6f7a8b9c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _tabla_existe(nombre: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return nombre in inspector.get_table_names()


def _columna_existe(tabla: str, columna: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return any(item["name"] == columna for item in inspector.get_columns(tabla))


def upgrade() -> None:
    if _tabla_existe("medicion_wifi") and not _tabla_existe("lectura_rssi"):
        op.rename_table("medicion_wifi", "lectura_rssi")

    if _tabla_existe("lectura_rssi"):
        for nombre, columna in (
            (
                "origen",
                sa.Column(
                    "origen",
                    sa.String(length=20),
                    nullable=False,
                    server_default="CAMPO",
                ),
            ),
            ("conjunto_ap_id", sa.Column("conjunto_ap_id", sa.Integer(), nullable=True)),
            ("mapa_calor_id", sa.Column("mapa_calor_id", sa.Integer(), nullable=True)),
            ("modelo_origen", sa.Column("modelo_origen", sa.String(length=60), nullable=True)),
            ("incertidumbre_db", sa.Column("incertidumbre_db", sa.Float(), nullable=True)),
        ):
            if not _columna_existe("lectura_rssi", nombre):
                op.add_column("lectura_rssi", columna)

        op.alter_column("lectura_rssi", "origen", server_default=None)
        op.create_index(
            "ix_lectura_rssi_origen",
            "lectura_rssi",
            ["origen"],
            unique=False,
            if_not_exists=True,
        )
        op.create_index(
            "ix_lectura_rssi_conjunto_ap_id",
            "lectura_rssi",
            ["conjunto_ap_id"],
            unique=False,
            if_not_exists=True,
        )
        op.create_index(
            "ix_lectura_rssi_mapa_calor_id",
            "lectura_rssi",
            ["mapa_calor_id"],
            unique=False,
            if_not_exists=True,
        )
        op.create_foreign_key(
            "fk_lectura_rssi_conjunto_ap",
            "lectura_rssi",
            "conjunto_ap",
            ["conjunto_ap_id"],
            ["id"],
            ondelete="CASCADE",
        )
        op.create_foreign_key(
            "fk_lectura_rssi_mapa_calor",
            "lectura_rssi",
            "mapa_calor",
            ["mapa_calor_id"],
            ["id"],
            ondelete="SET NULL",
        )

    if _tabla_existe("recomendacion_ap") and _columna_existe(
        "recomendacion_ap", "ap_fisico_id"
    ):
        op.drop_constraint(
            "fk_recomendacion_ap_ap_fisico",
            "recomendacion_ap",
            type_="foreignkey",
        )
        op.drop_index(
            "ix_recomendacion_ap_ap_fisico_id",
            table_name="recomendacion_ap",
            if_exists=True,
        )
        op.drop_column("recomendacion_ap", "ap_fisico_id")

    for tabla in ("bssid_radio", "radio_ap", "ap_fisico"):
        if _tabla_existe(tabla):
            op.drop_table(tabla)


def downgrade() -> None:
    if _tabla_existe("lectura_rssi"):
        for nombre in (
            "ix_lectura_rssi_mapa_calor_id",
            "ix_lectura_rssi_conjunto_ap_id",
            "ix_lectura_rssi_origen",
        ):
            op.drop_index(nombre, table_name="lectura_rssi", if_exists=True)
        for nombre in (
            "incertidumbre_db",
            "modelo_origen",
            "mapa_calor_id",
            "conjunto_ap_id",
            "origen",
        ):
            if _columna_existe("lectura_rssi", nombre):
                op.drop_column("lectura_rssi", nombre)
        if not _tabla_existe("medicion_wifi"):
            op.rename_table("lectura_rssi", "medicion_wifi")

    op.create_table(
        "ap_fisico",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("plano_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("fabricante", sa.String(length=100), nullable=False),
        sa.Column("modelo", sa.String(length=120), nullable=False),
        sa.Column("rol", sa.String(length=20), nullable=False, server_default="EXISTENTE"),
        sa.Column(
            "restriccion_movimiento",
            sa.String(length=20),
            nullable=False,
            server_default="MOVIBLE",
        ),
        sa.Column("coord_x", sa.Float(), nullable=False),
        sa.Column("coord_y", sa.Float(), nullable=False),
        sa.Column("altura_m", sa.Float(), nullable=False, server_default="2.5"),
        sa.Column("tipo_montaje", sa.String(length=30), nullable=False, server_default="TECHO"),
        sa.Column("verificado", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["plano_id"], ["plano.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_ap_fisico_plano_id", "ap_fisico", ["plano_id"])
    op.create_table(
        "radio_ap",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ap_fisico_id", sa.Integer(), nullable=False),
        sa.Column("banda", sa.String(length=10), nullable=False),
        sa.Column("habilitada", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("canal", sa.Integer(), nullable=False),
        sa.Column("ancho_canal_mhz", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("referencia_potencia", sa.String(length=15), nullable=False, server_default="IR"),
        sa.Column("potencia_dbm", sa.Float(), nullable=False),
        sa.Column("potencia_max_dbm", sa.Float(), nullable=False),
        sa.Column("tipo_antena", sa.String(length=30), nullable=False, server_default="OMNIDIRECCIONAL"),
        sa.Column("ganancia_dbi", sa.Float(), nullable=False, server_default="2.14"),
        sa.Column("perdida_cable_db", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["ap_fisico_id"], ["ap_fisico.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("ap_fisico_id", "banda", name="uq_radio_ap_banda"),
    )
    op.create_index("ix_radio_ap_ap_fisico_id", "radio_ap", ["ap_fisico_id"])
    op.create_table(
        "bssid_radio",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("radio_id", sa.Integer(), nullable=False),
        sa.Column("bssid", sa.String(length=17), nullable=False),
        sa.Column("ssid", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["radio_id"], ["radio_ap.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("bssid"),
    )
    op.create_index("ix_bssid_radio_radio_id", "bssid_radio", ["radio_id"])
    op.create_index("ix_bssid_radio_bssid", "bssid_radio", ["bssid"])
