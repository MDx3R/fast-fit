from fastfit.identity.domain.entity.identity import Identity
from fastfit.identity.domain.value_objects.password import Password
from fastfit.identity.domain.value_objects.username import Username
from fastfit.identity.infrastructure.database.postgres.sqlalchemy.models.identity_base import (
    IdentityBase,
)


class IdentityMapper:
    @classmethod
    def to_domain(cls, base: IdentityBase) -> Identity:
        return Identity(
            identity_id=base.identity_id,
            username=Username(base.username),
            password=Password(base.password) if base.password else None,
        )

    @classmethod
    def to_persistence(cls, user: Identity) -> IdentityBase:
        return IdentityBase(
            identity_id=user.identity_id,
            username=user.username.value,
            password=user.password.value if user.password else None,
        )
