import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    id: Optional[int] = Field(
        sa_column=Column(pg.INTEGER, nullable=False, unique=True, autoincrement=True)
    )
    username: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    email: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    first_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    last_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(
        sa_column=Column(pg.BOOLEAN, nullable=False, default=False)
    )
    is_active: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=False))
    hashed_password: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )

    def __repr__(self):
        return f"<User {self.username} - {self.email}>"
