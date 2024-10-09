"""user_profiles

Revision ID: 2399e36ed221
Revises: 2e1f47c5da46
Create Date: 2024-10-09 22:47:22.743476

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "2399e36ed221"
down_revision: Union[str, None] = "2e1f47c5da46"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_profiles",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("user_uid", sa.UUID(), nullable=False),
        sa.Column(
            "bio",
            sa.VARCHAR(),
            server_default="Tell the Bookly community a little about yourself! You can mention your favorite genres, what kinds of books you're currently reading or offering, and whether you're open to lending, borrowing, or selling books. Help others get to know your reading style and what you're looking for!",
            nullable=False,
        ),
        sa.Column(
            "avatar",
            sa.VARCHAR(),
            server_default="https://api.dicebear.com/9.x/adventurer-neutral/png?seed=Adrian",
            nullable=False,
        ),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_uid"],
            ["users.uid"],
        ),
        sa.PrimaryKeyConstraint("uid"),
    )


def downgrade() -> None:
    op.drop_table("user_profiles")
