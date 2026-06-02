from collections import defaultdict
from decimal import Decimal

from fastapi import Depends, HTTPException, status

from app.order_items.models import OrderItem
from app.orders.api.v1.schemas import ItemsRequest, ItemsResponse, OrderResponse
from app.uow import UnitOfWork, get_uow


class OrderService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_order(
        self, user_id: int, items: list[ItemsRequest]
    ) -> OrderResponse:
        grouped = defaultdict(int)

        # onli unique items
        for item in items:
            grouped[item.product_id] += item.quantity

        async with self.uow:
            order = self.uow.orders.create_new_order(user_id)

            products = await self.uow.products.get_products(list(grouped.keys()))

            missing_ids = set(grouped.keys()) - {p.id for p in products}

            if missing_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Products not found: {missing_ids}",
                )

            order_items: list[OrderItem] = list()
            for product in products:
                qty = grouped[product.id]

                if product.stock < qty:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Product {product.id} isn't enough stock,"
                            " available {product.stock}"
                        ),
                    )

                product.stock -= qty
                order_items.append(
                    OrderItem(
                        order=order,
                        product=product,
                        quantity=qty,
                        price_at_purchase=product.price,
                    )
                )

            await self.uow.items.add_items(order_items)
            await self.uow.flush()

            total = sum(item.price_at_purchase * item.quantity for item in order_items)

            # TODO
            response = OrderResponse(
                id=order.id,
                total=Decimal(total),
                items=[
                    ItemsResponse(
                        id=item.id, price=item.price_at_purchase, quantity=item.quantity
                    )
                    for item in order_items
                ],
            )

        return response


async def get_order_service(uow=Depends(get_uow)) -> OrderService:
    return OrderService(uow)
