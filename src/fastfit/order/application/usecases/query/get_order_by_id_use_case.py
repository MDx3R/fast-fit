from fastfit.order.application.dtos.queries.get_order_by_id_query import (
    GetOrderByIdQuery,
)
from fastfit.order.application.interfaces.repositories.order_read_repository import (
    IOrderReadRepository,
)
from fastfit.order.application.interfaces.usecases.query.get_order_by_id_use_case import (
    IGetOrderByIdUseCase,
)
from fastfit.order.application.read_models.order_read_model import OrderReadModel


class GetOrderByIdUseCase(IGetOrderByIdUseCase):
    def __init__(self, order_read_repository: IOrderReadRepository) -> None:
        self.order_read_repository = order_read_repository

    async def execute(self, query: GetOrderByIdQuery) -> OrderReadModel:
        return await self.order_read_repository.get_by_id(query.order_id)
