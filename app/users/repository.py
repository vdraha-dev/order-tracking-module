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

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def user_with_this_id_exists(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)

        if user:
            return True

        return False

    async def user_with_this_username_exists(self, username: str) -> bool:
        user = await self.get_user_by_username(username)

        if user:
            return True

        return False

    def add_user(self, user: User):
        self.session.add(user)


async def get_user_repository(session=Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)
