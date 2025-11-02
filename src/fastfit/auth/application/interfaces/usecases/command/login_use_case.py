from abc import ABC, abstractmethod

from fastfit.auth.application.dtos.commands.login_command import LoginCommand
from fastfit.auth.application.dtos.models.auth_tokens import AuthTokens


class ILoginUseCase(ABC):
    @abstractmethod
    async def execute(self, command: LoginCommand) -> AuthTokens: ...
