"""authors

Revision ID: 4dbd54902428
Revises: 80993e702d0c
Create Date: 2024-10-11 06:08:03.193956

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "4dbd54902428"
down_revision: Union[str, None] = "80993e702d0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.VARCHAR(), nullable=False),
        sa.Column("last_name", sa.VARCHAR(), nullable=False),
        sa.Column("pen_name", sa.VARCHAR(), nullable=True),
        sa.Column("nationality", sa.VARCHAR(), nullable=False),
        sa.Column("biography", sa.TEXT(), nullable=False),
        sa.Column(
            "profile_image",
            sa.VARCHAR(),
            server_default="https://api.dicebear.com/9.x/adventurer-neutral/png?seed=Adrian",
            nullable=True,
        ),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
    )


def downgrade() -> None:
    op.drop_table("authors")
