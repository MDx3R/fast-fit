from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.menu.domain.entities.dish import Dish


class IDishRepository(ABC):
    @abstractmethod
    async def get_by_id(self, dish_id: UUID) -> Dish: ...
    @abstractmethod
    async def add(self, entity: Dish) -> None: ...
    @abstractmethod
    async def save(self, entity: Dish) -> None: ...
    @abstractmethod
    async def delete(self, dish_id: UUID) -> None: ...
