import pytest

from src.config import settings
from src.database import db, get_async_engine


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # checking if we are in test mode
    assert settings.ENVIRONMENT == "TEST"
    engine = get_async_engine()
    async with engine.begin() as conn:
        # Drop all tables from the database
        await conn.run_sync(db.Model.metadata.drop_all)
        # Createing all tables from the database
        await conn.run_sync(db.Model.metadata.create_all)


@pytest.fixture(scope="function", autouse=True)
async def db_session():
    async with db.Session() as session:
        yield session
