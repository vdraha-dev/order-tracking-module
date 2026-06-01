from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from app.core.config import config
from app.users.api.v1.schemas import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
    UserLoginResponse,
)
from app.users.models import AccessToken, User
from app.users.repository import UserRepository, get_user_repository

hash_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate) -> UserCreateResponse:

        user_exists = await self.user_repository.user_with_this_email_exists(user.email)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        user_data = user.model_dump()
        user_data["password"] = self.hash_password(user_data["password"])

        db_user = User(**user_data)
        self.user_repository.add_object(db_user)
        await self.user_repository.flush()
        await self.user_repository.refresh_object(db_user)

        token, expire = self.generate_access_token(db_user)

        access_token = AccessToken(user_id=db_user.id, token=token, expires_at=expire)
        self.user_repository.add_object(access_token)

        await self.user_repository.commit()

        return UserCreateResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            access_token=token,
            expiry=expire,
        )

    async def handle_login(self, user: UserLogin):
        db_user = await self.user_repository.get_user_by_email(user.email)

        if not db_user or not hash_context.verify(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token, expiry = self.generate_access_token(db_user)

        access_token = AccessToken(user_id=db_user.id, token=token, expires_at=expiry)
        self.user_repository.add_object(access_token)

        await self.user_repository.commit()

        return UserLoginResponse(access_token=token, expiry=expiry)

    def hash_password(self, password: str) -> str:
        return hash_context.hash(password)

    def generate_access_token(self, user: User) -> tuple[str, datetime]:
        expire = datetime.now(tz=UTC) + timedelta(
            minutes=config.access_token_expire_minutes
        )

        payload = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "exp": expire,
        }

        token = jwt.encode(
            payload=payload, key=config.secret_key, algorithm=config.algorithm
        )

        return token, expire


async def get_user_service(user_repository=Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)
