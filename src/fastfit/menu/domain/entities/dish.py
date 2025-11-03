from dataclasses import dataclass
from typing import Self
from uuid import UUID

from fastfit.menu.domain.value_objects.dish_filters import DishFilters
from fastfit.menu.domain.value_objects.dish_name import DishName
from fastfit.menu.domain.value_objects.ingredients import Ingredients
from fastfit.menu.domain.value_objects.money import Money
from fastfit.menu.domain.value_objects.nutritional_info import NutritionalInfo


@dataclass
class Dish:
    dish_id: UUID
    name: DishName
    description: str
    price: Money
    nutritional_info: NutritionalInfo
    ingredients: Ingredients
    filters: DishFilters
    category_id: UUID
    restaurant_id: UUID
    image: str | None

    def update_name(self, name: DishName) -> None:
        self.name = name

    def update_description(self, description: str) -> None:
        self.description = description

    def update_price(self, price: Money) -> None:
        self.price = price

    def update_nutritional_info(self, nutritional_info: NutritionalInfo) -> None:
        self.nutritional_info = nutritional_info

    def update_ingredients(self, ingredients: Ingredients) -> None:
        self.ingredients = ingredients

    def update_filters(self, filters: DishFilters) -> None:
        self.filters = filters

    @classmethod
    def create(  # noqa: PLR0913
        cls,
        dish_id: UUID,
        name: DishName,
        description: str,
        price: Money,
        nutritional_info: NutritionalInfo,
        ingredients: Ingredients,
        filters: DishFilters,
        category_id: UUID,
        restaurant_id: UUID,
        image: str | None,
    ) -> Self:
        return cls(
            dish_id=dish_id,
            name=name,
            description=description,
            price=price,
            nutritional_info=nutritional_info,
            ingredients=ingredients,
            filters=filters,
            category_id=category_id,
            restaurant_id=restaurant_id,
            image=image,
        )
