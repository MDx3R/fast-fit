from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetDishByIdQuery:
    dish_id: UUID
