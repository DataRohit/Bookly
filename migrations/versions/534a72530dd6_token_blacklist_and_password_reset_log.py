"""token_blacklist_and_password_reset_log

Revision ID: 534a72530dd6
Revises: eb61d8e38af5
Create Date: 2024-10-09 04:48:11.479847

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "534a72530dd6"
down_revision: Union[str, None] = "eb61d8e38af5"
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
    op.create_table(
        "token_blacklist",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("token", sa.VARCHAR(), nullable=False),
        sa.Column("expires_at", postgresql.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("token"),
    )


def downgrade() -> None:
    op.drop_table("token_blacklist")
    op.drop_table("password_reset_log")
