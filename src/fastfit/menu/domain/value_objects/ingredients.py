from dataclasses import dataclass
from typing import Self

from common.domain.exceptions import InvariantViolationError


@dataclass(frozen=True)
class Ingredients:
    items: list[str]

    def __post_init__(self) -> None:
        if not self.items:
            raise InvariantViolationError("Ingredients list cannot be empty")

    @classmethod
    def create(cls, items: list[str]) -> Self:
        return cls(items=items)
