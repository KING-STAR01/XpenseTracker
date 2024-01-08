from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select

from typing import AsyncGenerator, List

from core.sesson import async_session
from schemas import UserSchema
from models import User

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def users_get(session: AsyncSession):
    async with session.begin():
        result = await session.execute(select(User))
        return result.scalars().all()


async def user_get(userid, session: AsyncSession):
    async with session.begin():
        result = await session.execute(select(User).where(User.user_id==userid))
        return result.scalars().first()


async def user_add(user: UserSchema, session: AsyncSession):
    async with session.begin():
        user_obj = User(**user.dict())
        session.add(user_obj)
        await session.flush()
        await session.refresh(user_obj)
        return user_obj

router = APIRouter()

@router.get("/users", response_model=List[UserSchema], status_code=status.HTTP_200_OK)
async def get_users(session: AsyncSession = Depends(get_session)):
    res = await users_get(session)
    return res

@router.get("/users/{userid}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user(userid, session: AsyncSession = Depends(get_session)):
    res = await user_get(userid, session)
    return res

@router.post("/add_user", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def add_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    res = await user_add(user, session)
    return res
    