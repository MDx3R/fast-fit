from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from fastfit.menu.domain.value_objects.dish_filters import DishFilterType


@dataclass
class CreateDishCommand:
    name: str
    description: str
    price: Decimal
    currency: str
    calories: Decimal
    proteins: Decimal
    fats: Decimal
    carbohydrates: Decimal
    ingredients: list[str]
    filters: list[DishFilterType]
    category_id: UUID
    restaurant_id: UUID
