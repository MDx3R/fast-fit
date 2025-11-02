from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.order.application.dtos.commands.create_order_command import (
    CreateOrderCommand,
)


class ICreateOrderUseCase(ABC):
    @abstractmethod
    async def execute(self, command: CreateOrderCommand) -> UUID: ...
