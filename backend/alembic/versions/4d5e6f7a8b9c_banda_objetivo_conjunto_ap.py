"""Agregar banda objetivo a conjunto_ap.

Revision ID: 4d5e6f7a8b9c
Revises: 3c4d5e6f7a8b
Create Date: 2026-06-28
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "4d5e6f7a8b9c"
down_revision: str | None = "3c4d5e6f7a8b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "conjunto_ap",
        sa.Column(
            "banda_objetivo",
            sa.String(length=10),
            nullable=False,
            server_default="5",
        ),
    )
    op.alter_column("conjunto_ap", "banda_objetivo", server_default=None)


def downgrade() -> None:
    op.drop_column("conjunto_ap", "banda_objetivo")
