import pytest
from httpx import AsyncClient
from sqlalchemy.sql import select

from src.users.models import User


@pytest.mark.asyncio
async def test_register_user(
    async_client: AsyncClient,
    db_session,
):
    TEST_EMAIL = "test@gmail.com"  # noqa
    response = await async_client.post(
        "/auth/signup",
        json={
            "email": TEST_EMAIL,
            "password": "test",
        },
    )

    assert response.status_code == 200
    result = await db_session.execute(select(User).where(User.email == TEST_EMAIL))
    user = result.scalar()
    assert user
