from fastapi import APIRouter, Depends, status

from app.orders.api.v1.schemas import ItemsRequest, OrderRequest, OrderResponse
from app.orders.service import OrderService, get_order_service
from app.users.api.v1.dependencies import get_current_user
from app.users.models import User

order = APIRouter(prefix="/order")


@order.post("/user", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def user_create_order(
    items: list[ItemsRequest],
    user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    data = await service.create_order(user.id, items)

    return data


@order.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order: OrderRequest,
    service: OrderService = Depends(get_order_service),
):
    data = await service.create_order(
        order.user_id, order.items, need_user_checking=True
    )
    return data


@order.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_order(): ...


@order.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order_by_id(): ...


@order.get(
    "/user/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK
)
async def get_orders_by_user_id(): ...
