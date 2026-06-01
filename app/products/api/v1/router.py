from fastapi import APIRouter, Depends, status

from app.products.api.v1.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.products.service import ProductService, get_product_service

product = APIRouter(prefix="/product")


@product.post(
    "/add", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def add_product(
    product: ProductCreate, service: ProductService = Depends(get_product_service)
):
    data = await service.add_product(product)
    return data


@product.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def remove_product(
    product_id: int, service: ProductService = Depends(get_product_service)
):
    data = await service.delete_product(product_id)
    return data


@product.get(
    "/all", response_model=list[ProductResponse], status_code=status.HTTP_200_OK
)
async def get_list_product(service: ProductService = Depends(get_product_service)):
    data = await service.get_products()
    return data


@product.patch(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service),
): ...
