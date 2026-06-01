
from fastapi import Depends, HTTPException, status

from app.products.api.v1.schemas import ProductCreate, ProductResponse
from app.products.models import Product
from app.products.repository import ProductRepository, get_product_repository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def add_product(self, product: ProductCreate) -> ProductResponse:
        db_product = Product(**product.model_dump())
        self.product_repository.add_product(db_product)
        await self.product_repository.flush()
        await self.product_repository.refresh_product(db_product)

        await self.product_repository.commit()

        return ProductResponse(id=db_product.id, **product.model_dump())

    async def delete_product(self, product_id: int) -> ProductResponse:
        product = await self.product_repository.remove_product(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return ProductResponse(
            id=product.id, name=product.name, price=product.price, stock=product.stock
        )

    async def get_products(self) -> list[ProductResponse]:
        products = await self.product_repository.get_all_products()

        return [
            ProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                stock=product.stock,
            )
            for product in products
        ]


async def get_product_service(
    repository=Depends(get_product_repository),
) -> ProductService:
    return ProductService(repository)
