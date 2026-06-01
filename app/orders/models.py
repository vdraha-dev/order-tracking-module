from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.order_items.models import OrderItem
    from app.users.models import User

from enum import StrEnum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OrderStatus(StrEnum):
    New = "new"
    Paid = "paid"
    Shipped = "shipped"
    Cancelled = "cancelled"


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    satus: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus), default=OrderStatus.New, nullable=False
    )

    # relationships

    user: Mapped[User] = relationship(back_populates="orders")

    items: Mapped[list[OrderItem]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
