from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.products.models import Product


@dataclass
class ProductInfo:
    price: Decimal
    stock: int


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add_product(self, product: Product):
        self.session.add(product)

    async def remove_product(self, product_id: int) -> Product | None:
        product = await self.session.get(Product, product_id)

        if product:
            await self.session.delete(product)

        return product

    async def get_products(self, ids: list[int] | None = None) -> Sequence[Product]:
        if not ids:
            stmt = select(Product)
        else:
            stmt = select(Product).where(Product.id.in_(ids))
        res = await self.session.execute(stmt)

        return res.scalars().all()


async def get_product_repository(session=Depends(get_session)) -> ProductRepository:
    return ProductRepository(session)
