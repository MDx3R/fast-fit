from fastfit.menu.application.read_models.dish_read_model import DishReadModel
from fastfit.menu.domain.value_objects.dish_filters import DishFilterType
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.mappers.category_read_mapper import (
    CategoryReadMapper,
)
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.models.models import (
    DishBase,
)


class DishReadMapper:
    @staticmethod
    def to_read_model(model: DishBase) -> DishReadModel:
        category = CategoryReadMapper.to_read_model(model.category)
        return DishReadModel(
            dish_id=model.dish_id,
            name=model.name,
            description=model.description,
            price=model.price,
            currency=model.currency,
            calories=model.calories,
            proteins=model.proteins,
            fats=model.fats,
            carbohydrates=model.carbohydrates,
            ingredients=model.ingredients,
            filters=[DishFilterType(f) for f in model.filters],
            category=category,
            restaurant_id=model.restaurant_id,
            image=model.image,
        )
