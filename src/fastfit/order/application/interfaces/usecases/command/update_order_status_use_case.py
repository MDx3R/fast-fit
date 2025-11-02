from abc import ABC, abstractmethod

from fastfit.order.application.dtos.commands.update_order_status_command import (
    UpdateOrderStatusCommand,
)


class IUpdateOrderStatusUseCase(ABC):
    @abstractmethod
    async def execute(self, command: UpdateOrderStatusCommand) -> None: ...
