from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.menu.application.read_models.category_read_model import CategoryReadModel


class ICategoryReadRepository(ABC):
    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> CategoryReadModel: ...
    @abstractmethod
    async def get_by_restaurant(
        self, restaurant_id: UUID
    ) -> list[CategoryReadModel]: ...
