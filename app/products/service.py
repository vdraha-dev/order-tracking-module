from fastapi import Depends, HTTPException, status

from app.products.api.v1.schemas import ProductCreate, ProductResponse
from app.products.models import Product
from app.uow import UnitOfWork, get_uow


class ProductService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_product(self, product: ProductCreate) -> ProductResponse:
        async with self.uow:
            db_product = Product(**product.model_dump())
            self.uow.products.add_product(db_product)
            await self.uow.flush()

            product_id = db_product.id
        return ProductResponse(id=product_id, **product.model_dump())

    async def delete_product(self, product_id: int) -> ProductResponse:
        async with self.uow:
            product = await self.uow.products.remove_product(product_id)

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
                )

            data = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
            }

        return ProductResponse(**data)

    async def get_products(self) -> list[ProductResponse]:
        async with self.uow:
            products = await self.uow.products.get_products()

            response = [
                ProductResponse(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    stock=product.stock,
                )
                for product in products
            ]

        return response


async def get_product_service(
    repository: UnitOfWork = Depends(get_uow),
) -> ProductService:
    return ProductService(repository)
