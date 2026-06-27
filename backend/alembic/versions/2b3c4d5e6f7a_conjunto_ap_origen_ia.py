"""Relacionar conjuntos IA con conjunto AP origen.

Revision ID: 2b3c4d5e6f7a
Revises: 1a2b3c4d5e6f
Create Date: 2026-06-27
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "2b3c4d5e6f7a"
down_revision: str | None = "1a2b3c4d5e6f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "conjunto_ap",
        sa.Column("conjunto_origen_id", sa.Integer(), nullable=True),
    )
    op.create_index(
        "ix_conjunto_ap_conjunto_origen_id",
        "conjunto_ap",
        ["conjunto_origen_id"],
    )
    op.create_foreign_key(
        "fk_conjunto_ap_origen",
        "conjunto_ap",
        "conjunto_ap",
        ["conjunto_origen_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_conjunto_ap_origen", "conjunto_ap", type_="foreignkey")
    op.drop_index("ix_conjunto_ap_conjunto_origen_id", table_name="conjunto_ap")
    op.drop_column("conjunto_ap", "conjunto_origen_id")
