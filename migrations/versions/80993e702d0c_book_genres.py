"""book_genres

Revision ID: 80993e702d0c
Revises: 851d8f474df1
Create Date: 2024-10-10 18:21:20.261148

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "80993e702d0c"
down_revision: Union[str, None] = "851d8f474df1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book_genres",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("genre", sa.VARCHAR(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=False),
        sa.Column("created_by", sa.UUID(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("genre"),
    )


def downgrade() -> None:
    op.drop_table("book_genres")
