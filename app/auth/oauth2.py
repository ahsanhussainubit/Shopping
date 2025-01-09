from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..auth import token
from ..model.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(requestToken: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    tokenData : TokenData = token.verify_token(requestToken, credentials_exception)
    return tokenData.user_id