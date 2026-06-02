from decimal import Decimal

from pydantic import BaseModel


class ItemsResponse(BaseModel):
    id: int
    price: Decimal
    quantity: int


class OrderResponse(BaseModel):
    id: int
    total: Decimal
    items: list[ItemsResponse]


class ItemsRequest(BaseModel):
    product_id: int
    quantity: int
