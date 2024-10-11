import uuid
from datetime import datetime

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Author(SQLModel, table=True):
    __tablename__ = "authors"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    first_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    last_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    pen_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
    nationality: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    biography: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    profile_image: str = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=True,
            server_default="https://api.dicebear.com/9.x/adventurer-neutral/png?seed=Adrian",
        )
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now
        )
    )
