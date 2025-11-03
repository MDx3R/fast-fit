from datetime import datetime
from decimal import Decimal
from uuid import UUID

from common.infrastructure.database.sqlalchemy.models.base import Base
from fastfit.order.domain.value_objects.delivery_type import DeliveryType
from fastfit.order.domain.value_objects.order_status import OrderStatus
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderItemBase(Base):
    __tablename__ = "order_items"

    order_id: Mapped[UUID] = mapped_column(
        PGUUID, ForeignKey("orders.order_id"), primary_key=True
    )
    dish_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)


class OrderBase(Base):
    __tablename__ = "orders"

    order_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    user_id: Mapped[UUID | None] = mapped_column(PGUUID, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False)
    delivery_type: Mapped[DeliveryType] = mapped_column(
        Enum(DeliveryType), nullable=False
    )
    delivery_address: Mapped[str | None] = mapped_column(String, nullable=True)
    restaurant_id: Mapped[UUID] = mapped_column(PGUUID, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    items: Mapped[list[OrderItemBase]] = relationship(
        "OrderItemBase", cascade="all, delete-orphan"
    )
