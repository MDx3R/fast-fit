from dataclasses import dataclass
from typing import Self

from common.domain.exceptions import InvariantViolationError


@dataclass(frozen=True)
class DishName:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvariantViolationError("Dish name must not be empty")

    @classmethod
    def create(cls, value: str) -> Self:
        return cls(value=value)
