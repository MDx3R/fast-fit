from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SendCodeCommand:
    phone_number: str


class ISendCodeUseCase(ABC):
    @abstractmethod
    async def execute(self, command: SendCodeCommand) -> None: ...
