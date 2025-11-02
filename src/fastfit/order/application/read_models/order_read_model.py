from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastfit.order.domain.value_objects.delivery_type import DeliveryType
from fastfit.order.domain.value_objects.order_status import OrderStatus


@dataclass(frozen=True)
class OrderItemReadModel:
    dish_id: UUID
    quantity: int
    price: Decimal
    currency: str


@dataclass(frozen=True)
class OrderReadModel:
    order_id: UUID
    user_id: UUID | None
    phone_number: str
    items: list[OrderItemReadModel]
    total_price: Decimal
    currency: str
    status: OrderStatus
    delivery_type: DeliveryType
    delivery_address: str | None
    restaurant_id: UUID
    created_at: datetime
