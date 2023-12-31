from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user

from ..database import get_async_db
from . import models as m
from . import schemas as s

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=List[s.UserBase])
async def get_users(
    db: AsyncSession = Depends(get_async_db),
    user: m.User = Depends(get_current_user),
):
    """Get all users"""
    users = await db.scalars(select(m.User))
    return users


@users_router.post("/", response_model=s.UserBase)
async def create_user(
    user: s.UserCreate,
    db: AsyncSession = Depends(get_async_db),
):
    """Create a new user"""
    user = m.User(**user.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@users_router.post("/sync", response_model=s.UserBase)
def create_user_sync(
    user: s.UserCreate,
    db: AsyncSession = Depends(get_async_db),
):
    """Create a new user"""
    user = m.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
