from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.repository.UserRepository import get_user_by_email
from .database import get_db
from sqlalchemy.orm import Session
from . import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(requestToken: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = token.verify_token(requestToken, credentials_exception)
    user = await get_user_by_email(email.username,db)
    return user