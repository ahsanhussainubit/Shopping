from ..model.schemas import CreateUser,ShowUser
from app.database import get_db
from app.model import models
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create(user: CreateUser, db: AsyncSession = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, sub = user.sub, network=user.network)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.id == id))
    user = result.scalar()
    if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return ShowUser(**user.__dict__)


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

async def get_user_by_sub(sub: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.sub == sub))
    return result.scalar()