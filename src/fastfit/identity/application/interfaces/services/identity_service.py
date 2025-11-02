from abc import ABC, abstractmethod
from uuid import UUID

from fastfit.identity.application.dtos.commands.create_identity_command import (
    CreateIdentityCommand,
)
from fastfit.identity.application.dtos.commands.verify_password_command import (
    VerifyPasswordCommand,
)
from fastfit.identity.domain.entity.identity import Identity


class IIdentityService(ABC):
    @abstractmethod
    async def exists_by_username(self, username: str) -> bool: ...
    @abstractmethod
    async def get_by_username(self, username: str) -> Identity: ...
    @abstractmethod
    async def verify_password(self, command: VerifyPasswordCommand) -> UUID: ...
    @abstractmethod
    async def create_identity(self, command: CreateIdentityCommand) -> UUID: ...
