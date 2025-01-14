from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..model.schemas import AuthRequest
from ..repository import AuthenticationRepository
from ..model import schemas
from ..database import get_db


router = APIRouter(tags=["Authentication"])

# @router.post("/login", response_model=schemas.Token)
# async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     return await AuthenticationRepository.login(request, db)

@router.post("/auth")
async def authenticate_user(request: AuthRequest,db: AsyncSession = Depends(get_db)):
    return await AuthenticationRepository.authenticate_user(request,db)


@router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    return await AuthenticationRepository.refresh_token(refresh_token,db)