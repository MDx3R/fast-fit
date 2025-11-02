from fastfit.menu.domain.entities.dish import Dish
from fastfit.menu.domain.value_objects.dish_filters import DishFilters, DishFilterType
from fastfit.menu.domain.value_objects.dish_name import DishName
from fastfit.menu.domain.value_objects.ingredients import Ingredients
from fastfit.menu.domain.value_objects.money import Money
from fastfit.menu.domain.value_objects.nutritional_info import NutritionalInfo
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.models.models import (
    DishBase,
)


class DishMapper:
    @staticmethod
    def to_domain(model: DishBase) -> Dish:
        return Dish.create(
            dish_id=model.dish_id,
            name=DishName.create(model.name),
            description=model.description,
            price=Money.create(model.price, model.currency),
            nutritional_info=NutritionalInfo.create(
                model.calories, model.proteins, model.fats, model.carbohydrates
            ),
            ingredients=Ingredients.create(model.ingredients),
            filters=DishFilters.create([DishFilterType(f) for f in model.filters]),
            category_id=model.category_id,
            restaurant_id=model.restaurant_id,
        )

    @staticmethod
    def to_persistence(entity: Dish) -> DishBase:
        return DishBase(
            dish_id=entity.dish_id,
            name=entity.name.value,
            description=entity.description,
            price=entity.price.amount,
            currency=entity.price.currency,
            calories=entity.nutritional_info.calories,
            proteins=entity.nutritional_info.proteins,
            fats=entity.nutritional_info.fats,
            carbohydrates=entity.nutritional_info.carbohydrates,
            ingredients=entity.ingredients.items,
            filters=[f.value for f in entity.filters.filters],
            category_id=entity.category_id,
            restaurant_id=entity.restaurant_id,
        )
