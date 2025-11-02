from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from fastfit.order.domain.value_objects.delivery_type import DeliveryType


@dataclass
class OrderItemDTO:
    dish_id: UUID
    quantity: int
    price: Decimal
    currency: str


@dataclass
class CreateOrderCommand:
    user_id: UUID | None
    phone_number: str
    items: list[OrderItemDTO]
    delivery_type: DeliveryType
    delivery_address: str | None
    restaurant_id: UUID
