from common.application.exceptions import NotFoundError
from common.domain.interfaces.clock import IClock
from fastfit.auth.application.dtos.models.auth_tokens import AuthTokens
from fastfit.auth.application.interfaces.repositories.token_repository import (
    IRefreshTokenRepository,
)
from fastfit.auth.application.interfaces.services.token_service import ITokenRefresher
from fastfit.auth.infrastructure.services.jwt.token_issuer import JWTTokenIssuer
from fastfit.auth.infrastructure.services.jwt.token_revoker import JWTTokenRevoker
from fastfit.identity.application.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
    TokenRevokedError,
)


class JWTTokenRefresher(ITokenRefresher):
    def __init__(
        self,
        clock: IClock,
        token_issuer: JWTTokenIssuer,
        token_revoker: JWTTokenRevoker,
        refresh_token_repository: IRefreshTokenRepository,
    ) -> None:
        self.clock = clock
        self.token_issuer = token_issuer
        self.token_revoker = token_revoker
        self.refresh_token_repository = refresh_token_repository

    async def refresh_tokens(self, refresh_token: str) -> AuthTokens:
        try:
            token = await self.refresh_token_repository.get(refresh_token)
        except NotFoundError as e:
            raise InvalidTokenError from e
        if token.is_expired(self.clock.now()):
            raise TokenExpiredError()
        if token.is_revoked():
            raise TokenRevokedError()

        await self.token_revoker.revoke_refresh_token(refresh_token)
        return await self.token_issuer.issue_tokens(token.identity_id)
