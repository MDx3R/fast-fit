from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.menu.application.dtos.commands.create_dish_command import CreateDishCommand


class ICreateDishUseCase(ABC):
    @abstractmethod
    async def execute(self, command: CreateDishCommand) -> UUID: ...
