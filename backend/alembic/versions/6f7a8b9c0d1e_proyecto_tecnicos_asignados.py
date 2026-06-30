"""Proyecto con técnicos asignados.

Sprint 6 — Portal cliente y operación colaborativa de campo.
"""

import sqlalchemy as sa

from alembic import op

revision: str = "6f7a8b9c0d1e"
down_revision: str | None = "5e6f7a8b9c0d"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "proyecto_tecnico_asignacion",
        sa.Column("proyecto_id", sa.Integer(), nullable=False),
        sa.Column("tecnico_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["proyecto_id"],
            ["proyecto.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tecnico_id"],
            ["usuario.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("proyecto_id", "tecnico_id"),
    )
    op.create_index(
        "ix_proyecto_tecnico_asignacion_tecnico_id",
        "proyecto_tecnico_asignacion",
        ["tecnico_id"],
        unique=False,
    )
    op.execute(
        """
        INSERT INTO proyecto_tecnico_asignacion (proyecto_id, tecnico_id)
        SELECT id, tecnico_id
        FROM proyecto
        ON CONFLICT DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_index(
        "ix_proyecto_tecnico_asignacion_tecnico_id",
        table_name="proyecto_tecnico_asignacion",
    )
    op.drop_table("proyecto_tecnico_asignacion")
