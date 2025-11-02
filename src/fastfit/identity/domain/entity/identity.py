from dataclasses import dataclass
from typing import Self
from uuid import UUID

from fastfit.identity.domain.value_objects.password import Password
from fastfit.identity.domain.value_objects.username import Username


@dataclass
class Identity:
    identity_id: UUID
    username: Username
    password: Password | None

    @classmethod
    def create(cls, identity_id: UUID, username: str, password: str | None) -> Self:
        return cls(
            identity_id=identity_id,
            username=Username(username),
            password=Password(password) if password else None,
        )
