from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from fastfit.menu.domain.entities.category import Category


@dataclass(frozen=True, kw_only=True)
class CategoryFactoryDTO:
    name: str
    restaurant_id: UUID


class ICategoryFactory(ABC):
    @abstractmethod
    def create(self, data: CategoryFactoryDTO) -> Category: ...
