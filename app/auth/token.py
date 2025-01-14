from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from ..model.models import RefreshToken
from ..database import get_db
from ..model.schemas import TokenData
from ..model.settings import settings
import secrets

# Constants
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate an access token with an optional expiration time.
    """
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception) -> TokenData:
    """
    Decode and verify the JWT access token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

async def verify_refresh_token(refresh_token: str,db: AsyncSession = Depends(get_db)):
    """
    Validate a refresh token and return the associated user ID.
    """
    try:
        user_id = await validate_refresh_token(refresh_token,db)
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

async def create_refresh_token(user_id: int,db: AsyncSession = Depends(get_db)) -> str:
    """
    Generate an opaque refresh token and store it in the database.
    """
    refresh_token = secrets.token_urlsafe(32)  # Generate a secure random token
    expires_at = (datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).replace(tzinfo=None)
    # Create a new refresh token entry
    new_token = RefreshToken(token=refresh_token, user_id=user_id, expires_at=expires_at, is_valid=True)
    db.add(new_token)
    await db.commit()
    await db.refresh(new_token)
    return refresh_token

async def validate_refresh_token(refresh_token: str,db: AsyncSession = Depends(get_db)) -> int:
    """
    Validate the refresh token and return the associated user ID.
    """
    try:
        # Fetch the token from the database
        query = select(RefreshToken).where(RefreshToken.token == refresh_token)
        result = await db.execute(query)
        token_data = result.scalar_one()

        # Check expiration
        if token_data.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            # Remove the expired token
            await revoke_refresh_token(refresh_token, db)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Refresh token expired"
            )
        return token_data.user_id
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid refresh token"
        )

async def revoke_refresh_token(refresh_token: str,db: AsyncSession = Depends(get_db)):
    """
    Revoke a refresh token by removing it from the database.
    """
    query = select(RefreshToken).where(RefreshToken.token == refresh_token)
    result = await db.execute(query)
    token_data = result.scalar_one_or_none()

    if token_data:
        await db.delete(token_data)
        await db.commit()
