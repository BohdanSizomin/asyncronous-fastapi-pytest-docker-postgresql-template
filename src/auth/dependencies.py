from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import UserNotFoundException
from .services import verify_access_token
from .schemas import TokenData
from src.logger import log
from src.users.models import User
from src.database import get_async_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)
) -> User:
    """Raises an exception if the current user is not authenticated"""
    token: TokenData = verify_access_token(token)
    user = db.query(User).filter_by(id=token.user_id).first()
    if not user:
        log(log.INFO, "User wasn`t authorized")
        raise UserNotFoundException
    return user
