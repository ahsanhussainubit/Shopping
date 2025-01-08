from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..repository import AuthenticationRepository
from ..model import schemas
from ..database import get_db


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await AuthenticationRepository.login(request, db)