"""password_reset_log

Revision ID: 2e1f47c5da46
Revises: 534a72530dd6
Create Date: 2024-10-10 04:04:19.461421

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "2e1f47c5da46"
down_revision: Union[str, None] = "534a72530dd6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "password_reset_log",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("user_email", sa.VARCHAR(), nullable=False),
        sa.Column("requested_at", postgresql.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
    )


def downgrade() -> None:
    op.drop_table("password_reset_log")
