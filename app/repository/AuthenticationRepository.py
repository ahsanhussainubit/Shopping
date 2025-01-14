import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
import requests
from google.oauth2 import id_token

from .UserRepository import get_user_by_sub
from ..auth import token
from ..auth.hashing import Hash
from ..model import models
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..model.schemas import AuthRequest, User, CreateUser
from ..model.settings import settings
from ..routes.UserRoute import create_user

# Configuration for providers
PROVIDERS = {
    "google": {
        "client_id": settings.google_client_id,
        "validation_url": None,  # Google uses public key verification
    },
    "facebook": {
        "validation_url": "https://graph.facebook.com/debug_token",
        "user_info_url": "https://graph.facebook.com/me",
    },
    "apple": {
        "client_id": settings.apple_client_id,
        "keys_url": "https://appleid.apple.com/auth/keys",
    },
}


async def login(request: OAuth2PasswordRequestForm, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.email == request.username))
    user = result.scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with email {request.username} not found"
        )
    if not Hash.verify(request.password, user.sub):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid password"
        )

    # Generate an access token
    access_token = token.create_access_token(data={"sub": str(user.id)})

    # Return the token response as a dictionary
    return {"access_token": access_token, "token_type": "bearer"}


async def authenticate_user(request: AuthRequest,db: AsyncSession = Depends(get_db)):
    """
    Generic function to authenticate users using any provider.
    """
    try:
        validate_fn = globals()[f"validate_{request.network}_token"]
        response : User = await validate_fn(request.token)

        # Check if the user already exists in the database
        user = await get_user_by_sub(response.sub,db)

        if not user:
            # If user doesn't exist, create a new user (signup)
            user = await create_user(CreateUser(name=response.name, email=response.email, sub=response.sub,network=request.network),db)

        # Create an access token using user identifier (`sub`)
        access_token = token.create_access_token(data={"sub": response.sub})

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def validate_google_token(token: str):
    """
    Validate Google ID token and retrieve user information.
    """
    client_id = PROVIDERS["google"]["client_id"]

    try:
        # Verify the token using Google's library
        id_info = id_token.verify_oauth2_token(token, requests.Request(), client_id)

        return User(sub=id_info["sub"], network="google", email=id_info["email"], name=id_info["email"].split("@")[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Google token: {str(e)}")


async def validate_facebook_token(token: str):
    """
    Validate Facebook user access token and retrieve user information.
    """
    user_info_url = PROVIDERS["facebook"]["user_info_url"]

    try:
        # Fetch user information directly using the provided token
        user_params = {
            "fields": "id,name,email",  # Fields to retrieve
            "access_token": token,  # Use user's access token directly
        }
        user_info_response = requests.get(user_info_url, params=user_params)
        user_info = user_info_response.json()

        # Check for errors in the response
        if "error" in user_info:
            raise HTTPException(
                status_code=400,
                detail=f"Error fetching Facebook user info: {user_info['error']}",
            )

        # Successfully retrieved user info
        return User(sub=user_info['id'], network="facebook", email=user_info['email'], name=user_info["email"].split("@")[0])

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error validating Facebook token: {str(e)}"
        )

async def validate_apple_token(id_token: str):
    """Validate Apple ID token and retrieve user information."""
    try:
        # Fetch Apple's public keys
        keys = requests.get(PROVIDERS["apple"]["keys_url"]).json()["keys"]

        # Get the unverified header from the JWT to find the kid (Key ID)
        unverified_header = jwt.get_unverified_header(id_token)
        if unverified_header is None or "kid" not in unverified_header:
            raise HTTPException(status_code=400, detail="Invalid ID token: missing key ID")

        # Find the correct public key using the key ID
        apple_key = next((key for key in keys if key["kid"] == unverified_header["kid"]), None)
        if apple_key is None:
            raise HTTPException(status_code=400, detail="Apple public key not found")

        # Create the RSA public key using modulus (n) and exponent (e)
        rsa_public_key = rsa.RSAPublicNumbers(
            int.from_bytes(base64.urlsafe_b64decode(apple_key["e"] + "=="), "big"),
            int.from_bytes(base64.urlsafe_b64decode(apple_key["n"] + "=="), "big"),
        ).public_key(default_backend())

        # Decode the JWT using the RSA public key and specify RS256 algorithm
        payload = jwt.decode(id_token, rsa_public_key, algorithms=["RS256"], audience=PROVIDERS["apple"]["client_id"])

        # Return the decoded payload (user information)
        return User(sub=payload["sub"], network="apple", email=payload["email"], name=payload["email"].split("@")[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")