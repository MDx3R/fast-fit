from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.identity.application.dtos.commands.create_identity_command import (
    CreateIdentityCommand,
)


class ICreateIdentityUseCase(ABC):
    @abstractmethod
    async def execute(self, command: CreateIdentityCommand) -> UUID: ...
