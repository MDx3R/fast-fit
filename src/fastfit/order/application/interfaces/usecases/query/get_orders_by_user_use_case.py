from abc import ABC, abstractmethod

from fastfit.order.application.dtos.queries.get_orders_by_user_query import (
    GetOrdersByUserQuery,
)
from fastfit.order.application.read_models.order_read_model import OrderReadModel


class IGetOrdersByUserUseCase(ABC):
    @abstractmethod
    async def execute(self, query: GetOrdersByUserQuery) -> list[OrderReadModel]: ...
