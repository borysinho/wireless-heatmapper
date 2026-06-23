"""descripcion_plano

Permite identificar el área o zona asociada a cada plano importado.

Revision ID: e9f0a1b2c3d4
Revises: d8e9f0a1b2c3
Create Date: 2026-06-23
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "e9f0a1b2c3d4"
down_revision: str | None = "d8e9f0a1b2c3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "plano",
        sa.Column("descripcion", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("plano", "descripcion")
