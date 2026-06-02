from typing import Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.order_items.repository import OrderItemRepository
from app.orders.repository import OrderRepository
from app.products.repository import ProductRepository
from app.users.repository import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.orders = OrderRepository(session)
        self.products = ProductRepository(session)
        self.items = OrderItemRepository(session)
        self.user = UserRepository(session)

    async def flush(self):
        await self.session.flush()

    async def refresh(self, obj: Any):
        await self.session.refresh(obj)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()


async def get_uof(session=Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session)
