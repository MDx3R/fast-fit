from fastfit.auth.application.dtos.models.auth_tokens import AuthTokens
from fastfit.auth.application.interfaces.services.token_service import ITokenIssuer
from fastfit.auth.application.interfaces.usecases.command.verify_code_use_case import (
    IVerifyCodeUseCase,
    VerifyCodeCommand,
)
from fastfit.identity.application.interfaces.services.identity_service import (
    IIdentityService,
)


class VerifyCodeUseCase(IVerifyCodeUseCase):
    def __init__(
        self,
        identity_service: IIdentityService,
        token_issuer: ITokenIssuer,
    ) -> None:
        self.identity_service = identity_service
        self.token_issuer = token_issuer

    async def execute(self, command: VerifyCodeCommand) -> AuthTokens:
        # NOTE: Check if exists, skip code verification
        identity = await self.identity_service.get_by_username(command.phone_number)
        return await self.token_issuer.issue_tokens(identity.identity_id)
