from dataclasses import dataclass
from typing import Self
from uuid import UUID

from common.domain.exceptions import InvariantViolationError
from fastfit.menu.domain.value_objects.money import Money


@dataclass
class OrderItem:
    dish_id: UUID
    quantity: int
    price: Money

    def __post_init__(self) -> None:
        if self.quantity < 1:
            raise InvariantViolationError("Quantity must be at least 1")

    @classmethod
    def create(cls, dish_id: UUID, quantity: int, price: Money) -> Self:
        return cls(dish_id=dish_id, quantity=quantity, price=price)
