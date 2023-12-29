from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_db
from src.logger import log
from src.users.models import User
from src.utils import create_hash

from .exceptions import UserCreationError
from .schemas import Login, SignUp, TokenData, TokenOut
from .services import create_access_token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/signup")
async def signup(
    data: SignUp,
    db: AsyncSession = Depends(get_async_db),
):
    """Signup user"""
    user = User(
        email=data.email,
        password=create_hash(data.password),
    )
    db.add(user)
    try:
        await db.commit()
    except Exception as e:
        log(log.INFO, "Error while signing up user: \n %s", e)
        raise UserCreationError
    return status.HTTP_201_CREATED


@auth_router.post("/login", response_model=TokenOut)
async def login(
    data: Login,
    db: AsyncSession = Depends(get_async_db),
):
    """Login user"""
    user = await User.authenticate(
        db=db,
        user_id=data.email,
        password=data.password,
    )
    token = create_access_token(TokenData(user_id=user.id))
    return TokenOut(access_token=token)
