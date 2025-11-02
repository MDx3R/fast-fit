from abc import ABC, abstractmethod

from fastfit.order.application.dtos.queries.get_order_by_id_query import (
    GetOrderByIdQuery,
)
from fastfit.order.application.read_models.order_read_model import OrderReadModel


class IGetOrderByIdUseCase(ABC):
    @abstractmethod
    async def execute(self, query: GetOrderByIdQuery) -> OrderReadModel: ...
