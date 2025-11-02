from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from fastfit.menu.application.read_models.category_read_model import CategoryReadModel
from fastfit.menu.domain.value_objects.dish_filters import DishFilterType


@dataclass(frozen=True)
class DishReadModel:
    dish_id: UUID
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
    category: CategoryReadModel
    restaurant_id: UUID
    image: str | None = None
