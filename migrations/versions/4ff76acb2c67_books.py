"""books

Revision ID: 4ff76acb2c67
Revises: 4dbd54902428
Create Date: 2024-10-12 15:25:48.205997

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "4ff76acb2c67"
down_revision: Union[str, None] = "4dbd54902428"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("title", sa.VARCHAR(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=False),
        sa.Column("isbn", sa.VARCHAR(), nullable=False),
        sa.Column("published_date", sa.DATE(), nullable=False),
        sa.Column("page_count", sa.INTEGER(), nullable=False),
        sa.Column("authors", postgresql.ARRAY(sa.UUID()), nullable=False),
        sa.Column("categories", postgresql.ARRAY(sa.UUID()), nullable=False),
        sa.Column("genres", postgresql.ARRAY(sa.UUID()), nullable=False),
        sa.Column("images", postgresql.ARRAY(sa.UUID()), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("isbn"),
    )


def downgrade() -> None:
    op.drop_table("books")
