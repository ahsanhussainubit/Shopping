from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import token
from ..auth.hashing import Hash
from ..model import models
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def login(request: OAuth2PasswordRequestForm, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.email == request.username))
    user = result.scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with email {request.username} not found"
        )
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid password"
        )

    # Generate an access token
    access_token = token.create_access_token(data={"sub": str(user.id)})

    # Return the token response as a dictionary
    return {"access_token": access_token, "token_type": "bearer"}
