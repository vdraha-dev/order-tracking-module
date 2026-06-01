from fastapi import APIRouter

from app.order_items.models import OrderItem
from app.orders.models import Order
from app.products.api.v1.router import product
from app.products.models import Product
from app.users.api.v1.router import auth
from app.users.models import AccessToken, User

api_version1_router = APIRouter(prefix="/api/v1")
api_version1_router.include_router(auth)
api_version1_router.include_router(product)


__all__ = ["User", "AccessToken", "Order", "OrderItem", "Product"]
