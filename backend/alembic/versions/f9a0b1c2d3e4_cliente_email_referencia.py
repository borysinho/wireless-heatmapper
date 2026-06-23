"""Correo de referencia para clientes.

Revision ID: f9a0b1c2d3e4
Revises: e9f0a1b2c3d4
Create Date: 2026-06-23
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f9a0b1c2d3e4"
down_revision: str | None = "e9f0a1b2c3d4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "cliente",
        sa.Column("email_referencia", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("cliente", "email_referencia")
