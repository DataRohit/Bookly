"""book_categories

Revision ID: 851d8f474df1
Revises: 2399e36ed221
Create Date: 2024-10-10 18:02:45.637223

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "851d8f474df1"
down_revision: Union[str, None] = "2399e36ed221"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book_categories",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("category", sa.VARCHAR(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=False),
        sa.Column("created_by", sa.UUID(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("category"),
    )


def downgrade() -> None:
    op.drop_table("book_categories")
