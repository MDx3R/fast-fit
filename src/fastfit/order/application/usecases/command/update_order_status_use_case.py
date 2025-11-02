from fastfit.order.application.dtos.commands.update_order_status_command import (
    UpdateOrderStatusCommand,
)
from fastfit.order.application.interfaces.repositories.order_repository import (
    IOrderRepository,
)
from fastfit.order.application.interfaces.usecases.command.update_order_status_use_case import (
    IUpdateOrderStatusUseCase,
)


class UpdateOrderStatusUseCase(IUpdateOrderStatusUseCase):
    def __init__(self, order_repository: IOrderRepository) -> None:
        self.order_repository = order_repository

    async def execute(self, command: UpdateOrderStatusCommand) -> None:
        order = await self.order_repository.get_by_id(command.order_id)
        order.update_status(command.status)
        await self.order_repository.update(order)
