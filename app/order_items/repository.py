from sqlalchemy.ext.asyncio import AsyncSession

from app.order_items.models import OrderItem


class OrderItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_items(self, items: list[OrderItem]):
        self.session.add_all(items)

    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()
