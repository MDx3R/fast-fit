from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from fastfit.menu.domain.value_objects.dish_filters import DishFilterType


@dataclass
class GetDishesByRestaurantQuery:
    restaurant_id: UUID
    filters: list[DishFilterType] | None = None
    max_calories: Decimal | None = None
