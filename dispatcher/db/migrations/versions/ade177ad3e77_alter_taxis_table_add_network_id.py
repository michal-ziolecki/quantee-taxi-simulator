"""alter taxis table add network_id

Revision ID: ade177ad3e77
Revises: bfc585f4f11d
Create Date: 2025-07-25 22:46:00.754066

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ade177ad3e77"
down_revision: Union[str, Sequence[str], None] = "bfc585f4f11d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "taxis", sa.Column("network_id", sa.String(), nullable=False, server_default="taxi")
    )


def downgrade() -> None:
    op.drop_column("taxis", "network_id")
