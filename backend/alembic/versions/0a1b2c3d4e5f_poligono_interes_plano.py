"""poligono_interes_plano

Almacena el área operativa delimitada por el técnico para heatmaps e IA.

Revision ID: 0a1b2c3d4e5f
Revises: f9a0b1c2d3e4
Create Date: 2026-06-23
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0a1b2c3d4e5f"
down_revision: str | None = "f9a0b1c2d3e4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("plano", sa.Column("poligono_interes", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("plano", "poligono_interes")
