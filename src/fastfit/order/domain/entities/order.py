from dataclasses import dataclass
from typing import Self
from uuid import UUID

from common.domain.exceptions import InvariantViolationError
from common.domain.value_objects.datetime import DateTime
from common.domain.value_objects.phone_number import PhoneNumber
from fastfit.order.domain.entities.order_item import OrderItem
from fastfit.order.domain.value_objects.delivery_address import DeliveryAddress
from fastfit.order.domain.value_objects.delivery_type import DeliveryType
from fastfit.order.domain.value_objects.order_status import OrderStatus


@dataclass
class Order:
    order_id: UUID
    user_id: UUID | None
    phone_number: PhoneNumber
    items: list[OrderItem]
    status: OrderStatus
    delivery_type: DeliveryType
    delivery_address: DeliveryAddress | None
    restaurant_id: UUID
    created_at: DateTime

    def __post_init__(self) -> None:
        if not self.items:
            raise InvariantViolationError("Order must contain at least one item")
        if (
            self.delivery_type == DeliveryType.DELIVERY
            and self.delivery_address is None
        ):
            raise InvariantViolationError(
                "Delivery address is required for delivery orders"
            )

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    def remove_item(self, dish_id: UUID) -> None:
        self.items = [item for item in self.items if item.dish_id != dish_id]
        if not self.items:
            raise InvariantViolationError("Order must contain at least one item")

    def update_status(self, status: OrderStatus) -> None:
        valid_transitions = {
            OrderStatus.CREATED: [OrderStatus.PREPARING],
            OrderStatus.PREPARING: [OrderStatus.READY],
            OrderStatus.READY: [OrderStatus.DELIVERED, OrderStatus.PICKED_UP],
        }
        if status not in valid_transitions.get(self.status, []):
            raise InvariantViolationError(
                f"Invalid status transition from {self.status} to {status}"
            )
        self.status = status

    @classmethod
    def create(  # noqa: PLR0913
        cls,
        order_id: UUID,
        user_id: UUID | None,
        phone_number: PhoneNumber,
        items: list[OrderItem],
        delivery_type: DeliveryType,
        delivery_address: DeliveryAddress | None,
        restaurant_id: UUID,
        created_at: DateTime,
    ) -> Self:
        return cls(
            order_id=order_id,
            user_id=user_id,
            phone_number=phone_number,
            items=items,
            status=OrderStatus.CREATED,
            delivery_type=delivery_type,
            delivery_address=delivery_address,
            restaurant_id=restaurant_id,
            created_at=created_at,
        )
