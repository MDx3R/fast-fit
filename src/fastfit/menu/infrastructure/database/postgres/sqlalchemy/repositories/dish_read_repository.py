from decimal import Decimal
from uuid import UUID

from common.infrastructure.database.sqlalchemy.executor import QueryExecutor
from fastfit.menu.application.interfaces.repositories.dish_read_repository import (
    IDishReadRepository,
)
from fastfit.menu.application.read_models.dish_read_model import DishReadModel
from fastfit.menu.domain.value_objects.dish_filters import DishFilterType
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.models.dish_base import (
    DishBase,
)
from sqlalchemy import select


class DishReadRepository(IDishReadRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, dish_id: UUID) -> DishReadModel:
        stmt = select(DishBase).where(DishBase.dish_id == dish_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Dish with id {dish_id} not found")
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
            category_id=model.category_id,
            restaurant_id=model.restaurant_id,
        )

    async def get_by_restaurant(self, restaurant_id: UUID) -> list[DishReadModel]:
        stmt = select(DishBase).where(DishBase.restaurant_id == restaurant_id)
        models = await self.executor.execute_scalar_many(stmt)
        return [
            DishReadModel(
                dish_id=m.dish_id,
                name=m.name,
                description=m.description,
                price=m.price,
                currency=m.currency,
                calories=m.calories,
                proteins=m.proteins,
                fats=m.fats,
                carbohydrates=m.carbohydrates,
                ingredients=m.ingredients,
                filters=[DishFilterType(f) for f in m.filters],
                category_id=m.category_id,
                restaurant_id=m.restaurant_id,
            )
            for m in models
        ]

    async def filter(
        self,
        restaurant_id: UUID,
        filters: list[DishFilterType],
        max_calories: Decimal | None,
    ) -> list[DishReadModel]:
        stmt = select(DishBase).where(DishBase.restaurant_id == restaurant_id)
        if filters:
            stmt = stmt.where(DishBase.filters.contains([f.value for f in filters]))
        if max_calories is not None:
            stmt = stmt.where(DishBase.calories <= max_calories)
        models = await self.executor.execute_scalar_many(stmt)
        return [
            DishReadModel(
                dish_id=m.dish_id,
                name=m.name,
                description=m.description,
                price=m.price,
                currency=m.currency,
                calories=m.calories,
                proteins=m.proteins,
                fats=m.fats,
                carbohydrates=m.carbohydrates,
                ingredients=m.ingredients,
                filters=[DishFilterType(f) for f in m.filters],
                category_id=m.category_id,
                restaurant_id=m.restaurant_id,
            )
            for m in models
        ]
