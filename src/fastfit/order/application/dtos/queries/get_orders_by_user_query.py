from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetOrdersByUserQuery:
    user_id: UUID
