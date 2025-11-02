from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from common.domain.exceptions import InvariantViolationError


@dataclass(frozen=True)
class NutritionalInfo:
    calories: Decimal
    proteins: Decimal
    fats: Decimal
    carbohydrates: Decimal

    def __post_init__(self) -> None:
        for field, value in [
            ("calories", self.calories),
            ("proteins", self.proteins),
            ("fats", self.fats),
            ("carbohydrates", self.carbohydrates),
        ]:
            if value < 0:
                raise InvariantViolationError(f"{field} cannot be negative")

    @classmethod
    def create(
        cls, calories: Decimal, proteins: Decimal, fats: Decimal, carbohydrates: Decimal
    ) -> Self:
        return cls(
            calories=calories, proteins=proteins, fats=fats, carbohydrates=carbohydrates
        )
