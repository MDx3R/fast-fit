from uuid import UUID

from common.infrastructure.database.sqlalchemy.executor import QueryExecutor
from fastfit.menu.application.interfaces.repositories.category_repository import (
    ICategoryRepository,
)
from fastfit.menu.domain.entities.category import Category
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.mappers.category_mapper import (
    CategoryMapper,
)


class CategoryRepository(ICategoryRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, category_id: UUID) -> Category:
        raise NotImplementedError()

    async def add(self, entity: Category) -> None:
        model = CategoryMapper.to_persistance(entity)
        await self.executor.add(model)

    async def save(self, entity: Category) -> None:
        model = CategoryMapper.to_persistance(entity)
        await self.executor.save(model)

    async def delete(self, category_id: UUID) -> None:
        raise NotImplementedError()
