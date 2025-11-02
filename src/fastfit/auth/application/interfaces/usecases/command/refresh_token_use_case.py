from abc import ABC, abstractmethod

from fastfit.auth.application.dtos.commands.refresh_token_command import (
    RefreshTokenCommand,
)
from fastfit.auth.application.dtos.models.auth_tokens import AuthTokens


class IRefreshTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, command: RefreshTokenCommand) -> AuthTokens: ...
