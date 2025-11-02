from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from fastfit.menu.domain.value_objects.dish_filters import DishFilterType


@dataclass
class UpdateDishCommand:
    dish_id: UUID
    name: str | None
    description: str | None
    price: Decimal | None
    currency: str | None
    calories: Decimal | None
    proteins: Decimal | None
    fats: Decimal | None
    carbohydrates: Decimal | None
    ingredients: list[str] | None
    filters: list[DishFilterType] | None
