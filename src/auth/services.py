from datetime import datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.users.models import User

from .exceptions import UserNotFoundException
from .schemas import TokenData, TokenOut


async def authenticate(
    db: AsyncSession,
    email: str,
) -> User:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise UserNotFoundException
    return user


def create_access_token(data: TokenOut) -> str:
    to_encode = data.dict()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET)
    return encoded_jwt


def verify_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET)
        id: int = payload.get("user_id")
        if not id:
            raise UserNotFoundException
        token_data = TokenData(user_id=id)
    except InvalidTokenError:
        raise InvalidTokenError
    return token_data
