from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from app.core.config import config
from app.uow import UnitOfWork, get_uow
from app.users.api.v1.schemas import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
    UserLoginResponse,
)
from app.users.models import AccessToken, User

hash_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, user: UserCreate) -> UserCreateResponse:

        async with self.uow:
            user_exists = await self.uow.user.user_with_this_email_exists(user.email)
            if user_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists",
                )

            user_data = user.model_dump()
            user_data["password"] = self.hash_password(user_data["password"])

            db_user = User(**user_data)
            self.uow.user.add_object(db_user)

            token, expire = self.generate_access_token(db_user)

            access_token = AccessToken(user=db_user, token=token, expires_at=expire)
            self.uow.user.add_object(access_token)

            await self.uow.flush()

            data = {
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email,
                "access_token": token,
                "expiry": expire,
            }

        return UserCreateResponse(**data)

    async def handle_login(self, user: UserLogin):
        async with self.uow:
            db_user = await self.uow.user.get_user_by_email(user.email)

            if not db_user or not hash_context.verify(user.password, db_user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token, expiry = self.generate_access_token(db_user)

            access_token = AccessToken(
                user_id=db_user.id, token=token, expires_at=expiry
            )
            self.uow.user.add_object(access_token)

            data = {"access_token": token, "expiry": expiry}

        return UserLoginResponse(**data)

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


async def get_user_service(uow=Depends(get_uow)) -> UserService:
    return UserService(uow=uow)
