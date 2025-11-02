from uuid import UUID

from common.infrastructure.database.sqlalchemy.executor import QueryExecutor
from fastfit.menu.application.interfaces.repositories.dish_repository import (
    IDishRepository,
)
from fastfit.menu.domain.entities.dish import Dish
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.mappers.dish_mapper import (
    DishMapper,
)
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.models.dish_base import (
    DishBase,
)
from sqlalchemy import delete, select


class DishRepository(IDishRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, dish_id: UUID) -> Dish:
        stmt = select(DishBase).where(DishBase.dish_id == dish_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Dish with id {dish_id} not found")
        return DishMapper.to_domain(model)

    async def add(self, entity: Dish) -> None:
        model = DishMapper.to_persistence(entity)
        await self.executor.add(model)

    async def save(self, entity: Dish) -> None:
        model = DishMapper.to_persistence(entity)
        await self.executor.save(model)

    async def delete(self, dish_id: UUID) -> None:
        stmt = delete(DishBase).where(DishBase.dish_id == dish_id)
        await self.executor.execute(stmt)
