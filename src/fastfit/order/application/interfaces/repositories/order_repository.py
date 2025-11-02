from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.order.domain.entities.order import Order


class IOrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order: ...

    @abstractmethod
    async def add(self, entity: Order) -> None: ...

    @abstractmethod
    async def update(self, entity: Order) -> None: ...
