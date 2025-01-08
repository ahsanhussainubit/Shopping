from fastapi import APIRouter
from ..repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from fastapi import Depends
from ..schemas import User

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id:int,db: AsyncSession = Depends(get_db)):
    return await UserRepository.get_one(user_id,db)

@router.post("")
async def create_user(user:User,db: AsyncSession = Depends(get_db)):
    return await UserRepository.create(user,db)