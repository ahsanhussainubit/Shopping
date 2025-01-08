from fastapi import APIRouter
from ..repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from fastapi import Depends
from ..schemas import CreateUser,ShowUser
from ..oauth2 import get_current_user

router = APIRouter(prefix="/users",tags=["users"])

@router.get("")
async def get_user_by_id(user_id:int|None = None,db: AsyncSession = Depends(get_db),user:ShowUser = Depends(get_current_user)):
    if user_id is None:
        user_id = user.id
    return await UserRepository.get_one(user_id,db)

@router.post("")
async def create_user(user:CreateUser,db: AsyncSession = Depends(get_db)):
    return await UserRepository.create(user,db)