from decimal import Decimal
from uuid import UUID

from common.infrastructure.database.sqlalchemy.executor import QueryExecutor
from fastfit.menu.application.interfaces.repositories.dish_read_repository import (
    IDishReadRepository,
)
from fastfit.menu.application.read_models.dish_read_model import DishReadModel
from fastfit.menu.domain.value_objects.dish_filters import DishFilterType
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.mappers.dish_read_mapper import (
    DishReadMapper,
)
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.models.models import (
    DishBase,
)
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class DishReadRepository(IDishReadRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, dish_id: UUID) -> DishReadModel:
        stmt = (
            select(DishBase)
            .options(joinedload(DishBase.category))
            .where(DishBase.dish_id == dish_id)
        )
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Dish with id {dish_id} not found")
        return DishReadMapper.to_read_model(model)

    async def get_by_restaurant(self, restaurant_id: UUID) -> list[DishReadModel]:
        stmt = (
            select(DishBase)
            .options(joinedload(DishBase.category))
            .where(DishBase.restaurant_id == restaurant_id)
        )
        models = await self.executor.execute_scalar_many(stmt)
        return [DishReadMapper.to_read_model(m) for m in models]

    async def filter(
        self,
        restaurant_id: UUID,
        filters: list[DishFilterType],
        max_calories: Decimal | None,
    ) -> list[DishReadModel]:
        stmt = (
            select(DishBase)
            .options(joinedload(DishBase.category))
            .where(DishBase.restaurant_id == restaurant_id)
        )
        if filters:
            stmt = stmt.where(DishBase.filters.contains([f.value for f in filters]))
        if max_calories is not None:
            stmt = stmt.where(DishBase.calories <= max_calories)
        models = await self.executor.execute_scalar_many(stmt)
        return [DishReadMapper.to_read_model(m) for m in models]
