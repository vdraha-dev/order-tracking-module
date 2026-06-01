import os

import jwt
from alembic.util import status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.users.models import User
from app.users.repository import UserRepository, get_user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        email = payload.get("email")

        if not email:
            raise credential_exception

    except jwt.InvalidTokenError:
        raise credential_exception from None

    user = await user_repository.get_user_by_email(email)
    if not user:
        raise credential_exception

    return user
