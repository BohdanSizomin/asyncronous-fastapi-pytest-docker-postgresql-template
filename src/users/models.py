from typing import Self
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func, or_

from src.auth.exceptions import IncorrectEmailOrPasswordException
from src.database import db
from src.utils import create_hash, verify_hash


class User(db.Model):
    __tablename__ = "user"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
    )
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String,
        default=lambda: str(uuid4()),
        unique=True,
    )
    email: orm.Mapped[str] = orm.mapped_column(
        sa.String,
        unique=True,
    )
    hashed_password: orm.Mapped[str] = orm.mapped_column(
        sa.String,
    )

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, value: str):
        self.hashed_password = create_hash(value)

    @classmethod
    async def authenticate(cls, db: AsyncSession, user_id: str, password: str) -> Self:
        query = select(cls).where(
            or_(
                func.lower(cls.email) == func.lower(user_id),
            )
        )
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if user is not None and verify_hash(password, user.password):
            raise IncorrectEmailOrPasswordException
        return user

    def __str__(self):
        return f"{self.id}-{self.email}"
