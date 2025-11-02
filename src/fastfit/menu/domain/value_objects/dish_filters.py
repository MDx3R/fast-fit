from dataclasses import dataclass
from enum import Enum
from typing import Self


class DishFilterType(Enum):
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    SPORTS_MENU = "sports_menu"


@dataclass(frozen=True)
class DishFilters:
    filters: list[DishFilterType]

    @classmethod
    def create(cls, filters: list[DishFilterType]) -> Self:
        return cls(filters=filters)
