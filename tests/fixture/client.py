import asyncio

import pytest
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return "some-seed"


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
