from fastapi import APIRouter, Depends, status

from app.orders.api.v1.schemas import OrderRequest, OrderResponse
from app.orders.service import OrderService, get_order_service

order = APIRouter(prefix="/order")


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


# @order.delete("/{order_id}", status_code=status.HTTP_200_OK)
# async def delete_order(): ...


# @order.get(
#     "/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK
# )
# async def get_order_by_id(): ...


@order.get(
    "/user/{user_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK
)
async def get_orders_by_user_id(): ...
