from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CategoryReadModel:
    category_id: UUID
    name: str
    restaurant_id: UUID
