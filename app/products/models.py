from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.order_items.models import OrderItem

from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # relationships

    order_items: Mapped[list[OrderItem]] = relationship(back_populates="product")
