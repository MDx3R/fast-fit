from enum import Enum
from typing import ClassVar

from common.infrastructure.app.http_app import IHTTPApp
from common.infrastructure.server.fastapi.server import FastAPIServer
from fastfit.identity.application.interfaces.services.token_intospector import (
    ITokenIntrospector,
)
from fastfit.identity.application.interfaces.usecases.command.create_identity_use_case import (
    ICreateIdentityUseCase,
)
from fastfit.identity.infrastructure.di.container.container import IdentityContainer


class IdentityApp(IHTTPApp):
    prefix = "/users"
    tags: ClassVar[list[str | Enum]] = ["Users"]

    def __init__(
        self,
        identity_container: IdentityContainer,
        server: FastAPIServer,
    ) -> None:
        self.identity_container = identity_container
        self.server = server

    def configure_dependencies(self) -> None:
        self.server.override_dependency(
            ICreateIdentityUseCase, self.identity_container.create_identity_use_case()
        )
        self.server.override_dependency(
            ITokenIntrospector, self.identity_container.token_introspector()
        )

    def register_routers(self) -> None: ...
