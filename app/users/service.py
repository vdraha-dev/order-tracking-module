from fastapi import Depends, HTTPException, status

from app.uow import UnitOfWork, get_uow
from app.users.api.v1.schemas import (
    UserCreate,
    UserCreateResponse,
)
from app.users.models import User


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, user: UserCreate) -> UserCreateResponse:

        async with self.uow:
            user_exists = await self.uow.user.user_with_this_username_exists(
                user.username
            )
            if user_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this username already exists",
                )

            user_data = user.model_dump()

            db_user = User(**user_data)
            self.uow.user.add_user(db_user)

            await self.uow.flush()

            data = {
                "id": db_user.id,
                "username": db_user.username,
            }

        return UserCreateResponse(**data)


async def get_user_service(uow=Depends(get_uow)) -> UserService:
    return UserService(uow=uow)
