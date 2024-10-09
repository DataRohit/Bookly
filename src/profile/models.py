import uuid
from datetime import datetime

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, ForeignKey, SQLModel


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("users.uid"), nullable=False)
    )
    bio: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    avatar: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now
        )
    )
