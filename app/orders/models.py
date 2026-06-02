from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.order_items.models import OrderItem
    from app.users.models import User

from enum import StrEnum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, func, select
from sqlalchemy.ext.hybrid import hybrid_property
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

    @hybrid_property
    def total(self) -> Decimal:  # type: ignore
        return Decimal(
            sum(item.price_at_purchase * item.quantity for item in self.items)
        )

    @total.expression
    def total(cls):
        return (
            select(
                func.coalesce(
                    func.sum(OrderItem.price_at_purchase * OrderItem.quantity), 0
                )
            )
            .where(OrderItem.order_id == cls.id)
            .scalar_subquery()
        )

    # relationships

    user: Mapped[User] = relationship(back_populates="orders")

    items: Mapped[list[OrderItem]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
