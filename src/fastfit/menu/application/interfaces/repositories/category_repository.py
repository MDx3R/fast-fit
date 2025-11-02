from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.menu.domain.entities.category import Category


class ICategoryRepository(ABC):
    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Category: ...
    @abstractmethod
    async def add(self, entity: Category) -> None: ...
    @abstractmethod
    async def update(self, entity: Category) -> None: ...
    @abstractmethod
    async def delete(self, category_id: UUID) -> None: ...
