from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from fastfit.menu.application.read_models.dish_read_model import DishReadModel
from fastfit.menu.domain.value_objects.dish_filters import DishFilterType


class IDishReadRepository(ABC):
    @abstractmethod
    async def get_by_id(self, dish_id: UUID) -> DishReadModel: ...
    @abstractmethod
    async def get_by_restaurant(self, restaurant_id: UUID) -> list[DishReadModel]: ...
    @abstractmethod
    async def filter(
        self,
        restaurant_id: UUID,
        filters: list[DishFilterType],
        max_calories: Decimal | None,
    ) -> list[DishReadModel]: ...
