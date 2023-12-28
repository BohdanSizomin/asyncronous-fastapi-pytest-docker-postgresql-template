from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import orm

from src.database import db


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
    password: orm.Mapped[str] = orm.mapped_column(
        sa.String,
    )

    def __str__(self):
        return f"{self.id}-{self.email}"
