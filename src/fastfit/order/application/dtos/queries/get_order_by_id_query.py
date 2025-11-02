from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetOrderByIdQuery:
    order_id: UUID
