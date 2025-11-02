from fastfit.order.application.dtos.queries.get_orders_by_user_query import (
    GetOrdersByUserQuery,
)
from fastfit.order.application.interfaces.repositories.order_read_repository import (
    IOrderReadRepository,
)
from fastfit.order.application.interfaces.usecases.query.get_orders_by_user_use_case import (
    IGetOrdersByUserUseCase,
)
from fastfit.order.application.read_models.order_read_model import OrderReadModel


class GetOrdersByUserUseCase(IGetOrdersByUserUseCase):
    def __init__(self, order_read_repository: IOrderReadRepository) -> None:
        self.order_read_repository = order_read_repository

    async def execute(self, query: GetOrdersByUserQuery) -> list[OrderReadModel]:
        return await self.order_read_repository.get_by_user(query.user_id)
