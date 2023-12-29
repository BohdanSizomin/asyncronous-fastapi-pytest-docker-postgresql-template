from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.database import get_async_db
from src.logger import log
from src.users.models import User

from .exceptions import UserNotFoundException
from .schemas import TokenData
from .services import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db),
) -> User:
    """Raises an exception if the current user is not authenticated"""
    token: TokenData = verify_access_token(token)
    stmnt = select(User).where(User.id == token.user_id)
    result = await db.execute(stmnt)
    user = result.scalars().first()
    if not user:
        log(log.INFO, "User wasn`t authorized")
        raise UserNotFoundException
    return user
