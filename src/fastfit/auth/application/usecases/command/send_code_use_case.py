from fastfit.auth.application.interfaces.usecases.command.send_code_use_case import (
    ISendCodeUseCase,
    SendCodeCommand,
)


class SendCodeUseCase(ISendCodeUseCase):
    async def execute(self, command: SendCodeCommand) -> None: ...
