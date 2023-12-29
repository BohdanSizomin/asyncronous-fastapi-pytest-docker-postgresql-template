from datetime import datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.users.models import User
from src.utils import verify_hash

from .exceptions import IncorrectEmailOrPasswordException, UserNotFoundException
from .schemas import TokenData, TokenOut


async def authenticate(
    db: AsyncSession,
    email: str,
    password: str,
) -> User:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise UserNotFoundException
    if not verify_hash(password, user.password):
        raise IncorrectEmailOrPasswordException
    return user


def create_access_token(data: TokenOut) -> str:
    to_encode = data.model_dump()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET)
    return encoded_jwt


def verify_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        id: int = payload.get("user_id")
        if not id:
            raise UserNotFoundException
        token_data = TokenData(user_id=id)
    except InvalidTokenError:
        raise InvalidTokenError
    return token_data
