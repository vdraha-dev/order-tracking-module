from typing import Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_user_by_email(self, user_email: str) -> User | None:
        stmt = select(User).where(User.email == user_email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def user_with_this_email_exists(self, user_email: str) -> bool:
        user = await self.get_user_by_email(user_email)

        if user:
            return True

        return False

    def add_object(self, obj: Any):
        self.session.add(obj)

    async def flush(self):
        await self.session.flush()

    async def refresh_object(self, obj):
        await self.session.refresh(obj)

    async def commit(self):
        await self.session.commit()

    # async def add_access_token(self, token: AccessToken):
    #     self.session.add(token)

    # async def add_user(self, user: User):
    #     self.session.add(user)


async def get_user_repository(session=Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)
