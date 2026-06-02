from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.orders.models import Order

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)

    # relationships

    orders: Mapped[list[Order]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
