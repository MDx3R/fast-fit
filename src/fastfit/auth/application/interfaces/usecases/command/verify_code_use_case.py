from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastfit.auth.application.dtos.models.auth_tokens import AuthTokens


@dataclass(frozen=True)
class VerifyCodeCommand:
    phone_number: str
    code: str


class IVerifyCodeUseCase(ABC):
    @abstractmethod
    async def execute(self, command: VerifyCodeCommand) -> AuthTokens: ...
