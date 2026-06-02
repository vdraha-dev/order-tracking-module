from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_session
from app.orders.models import Order


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create_new_order(self, user_id: int) -> Order:
        order = Order(user_id=user_id)
        self.session.add(order)
        return order

    async def get_orders_by_user_id(self, user_id: int) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
        )

        res = await self.session.execute(stmt)

        return list(res.scalars().all())


async def get_order_repository(session=Depends(get_session)) -> OrderRepository:
    return OrderRepository(session)
