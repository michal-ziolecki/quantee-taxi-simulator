"""Initial Schema

Revision ID: bfc585f4f11d
Revises:
Create Date: 2025-07-24 22:00:52.917118

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "bfc585f4f11d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "taxis",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column(
            "status", sa.Enum("available", "busy", "off", name="taxi_status"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_taxis_id"), "taxis", ["id"], unique=False)
    op.create_table(
        "trips",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("taxi_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("pickup_x", sa.Integer(), nullable=False),
        sa.Column("pickup_y", sa.Integer(), nullable=False),
        sa.Column("dropoff_x", sa.Integer(), nullable=False),
        sa.Column("dropoff_y", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), default=sa.func.now(), nullable=False),
        sa.Column("pickup_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("dropoff_time", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["taxi_id"],
            ["taxis.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_trips_id"), "trips", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_trips_id"), table_name="trips")
    op.drop_table("trips")
    op.drop_index(op.f("ix_taxis_id"), table_name="taxis")
    op.drop_table("taxis")
    op.execute("DROP TYPE IF EXISTS taxi_status;")
