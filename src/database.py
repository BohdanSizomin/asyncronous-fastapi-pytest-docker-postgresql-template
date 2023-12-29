from functools import lru_cache
from typing import Generator

from alchemical.aio import Alchemical
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.pool import NullPool

from .config import settings

DATABASE_URL = (
    settings.DATABASE_URL
    if settings.ENVIRONMENT != "TEST"
    else settings.TEST_DATABASE_URL
)

db: Alchemical = Alchemical(
    settings.DATABASE_URL,
    session_options={
        "expire_on_commit": False,
        "autocommit": False,
        "autoflush": False,
    },
    engine_options={"poolclass": NullPool} if settings.ENVIRONMENT == "TEST" else {},
)


@lru_cache
def get_async_engine() -> AsyncEngine:
    return db.get_engine()


async def get_async_db() -> Generator[AsyncSession, None, None]:
    async with db.Session() as session:
        try:
            yield session
        except:  # noqa
            await session.rollback()
            raise
        finally:
            await session.close()
