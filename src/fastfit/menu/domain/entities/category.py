from dataclasses import dataclass
from typing import Self
from uuid import UUID

from fastfit.menu.domain.value_objects.category_name import CategoryName


@dataclass
class Category:
    category_id: UUID
    name: CategoryName
    restaurant_id: UUID

    def update_name(self, name: CategoryName) -> None:
        self.name = name

    @classmethod
    def create(cls, category_id: UUID, name: CategoryName, restaurant_id: UUID) -> Self:
        return cls(category_id=category_id, name=name, restaurant_id=restaurant_id)
