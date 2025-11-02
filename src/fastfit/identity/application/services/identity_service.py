from uuid import UUID

from common.application.exceptions import DuplicateEntryError
from fastfit.identity.application.dtos.commands.create_identity_command import (
    CreateIdentityCommand,
)
from fastfit.identity.application.dtos.commands.verify_password_command import (
    VerifyPasswordCommand,
)
from fastfit.identity.application.exceptions import (
    InvalidPasswordError,
    InvalidUsernameError,
    UsernameAlreadyTakenError,
)
from fastfit.identity.application.interfaces.repositories.identity_repository import (
    IIdentityRepository,
)
from fastfit.identity.application.interfaces.services.identity_service import (
    IIdentityService,
)
from fastfit.identity.application.interfaces.services.password_hash_service import (
    IPasswordHasher,
)
from fastfit.identity.domain.entity.identity import Identity
from fastfit.identity.domain.interfaces.identity_factory import IIdentityFactory


class IdentityService(IIdentityService):
    def __init__(
        self,
        identity_repository: IIdentityRepository,
        identity_factory: IIdentityFactory,
        password_hasher: IPasswordHasher,
    ) -> None:
        self.identity_repository = identity_repository
        self.identity_factory = identity_factory
        self.password_hasher = password_hasher

    async def exists_by_username(self, username: str) -> bool:
        return await self.identity_repository.exists_by_username(username)

    async def get_by_username(self, username: str) -> Identity:
        return await self.identity_repository.get_by_username(username)

    async def create_identity(self, command: CreateIdentityCommand) -> UUID:
        if await self.exists_by_username(command.username):
            raise UsernameAlreadyTakenError(command.username)

        password_hash = self.password_hasher.hash(command.password)
        identity = self.identity_factory.create(command.username, password_hash)

        try:
            await self.identity_repository.add(identity)
        except DuplicateEntryError as exc:
            raise UsernameAlreadyTakenError(command.username) from exc

        return identity.identity_id

    async def verify_password(self, command: VerifyPasswordCommand) -> UUID:
        if not await self.exists_by_username(command.username):
            raise InvalidUsernameError(command.username)

        identity = await self.get_by_username(command.username)
        if not identity.password:
            raise InvalidPasswordError(identity.identity_id)
        if not (
            identity.password
            and self.password_hasher.verify(command.password, identity.password.value)
        ):
            raise InvalidPasswordError(identity.identity_id)

        return identity.identity_id
