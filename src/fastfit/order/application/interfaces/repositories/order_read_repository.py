from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.order.application.read_models.order_read_model import OrderReadModel
from fastfit.order.domain.value_objects.order_status import OrderStatus


class IOrderReadRepository(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> OrderReadModel: ...

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> list[OrderReadModel]: ...

    @abstractmethod
    async def get_by_restaurant(
        self, restaurant_id: UUID, status: OrderStatus | None
    ) -> list[OrderReadModel]: ...
