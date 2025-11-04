from enum import Enum
from typing import ClassVar

from common.infrastructure.app.http_app import IHTTPApp
from common.infrastructure.server.fastapi.server import FastAPIServer
from fastfit.order.application.interfaces.usecases.command.create_order_use_case import (
    ICreateOrderUseCase,
)
from fastfit.order.application.interfaces.usecases.command.update_order_status_use_case import (
    IUpdateOrderStatusUseCase,
)
from fastfit.order.application.interfaces.usecases.query.get_order_by_id_use_case import (
    IGetOrderByIdUseCase,
)
from fastfit.order.application.interfaces.usecases.query.get_orders_by_user_use_case import (
    IGetOrdersByUserUseCase,
)
from fastfit.order.infrastructure.di.container.container import OrderContainer
from fastfit.order.presentation.http.fastapi.controllers import order_router


class OrderApp(IHTTPApp):
    prefix = ""
    tags: ClassVar[list[str | Enum]] = ["Orders"]

    def __init__(
        self,
        order_container: OrderContainer,
        server: FastAPIServer,
    ) -> None:
        self.order_container = order_container
        self.server = server

    def configure_dependencies(self) -> None:
        self.server.override_dependency(
            ICreateOrderUseCase, self.order_container.create_order_use_case()
        )
        self.server.override_dependency(
            IUpdateOrderStatusUseCase, self.order_container.update_order_use_case()
        )
        self.server.override_dependency(
            IGetOrderByIdUseCase, self.order_container.get_order_by_id_use_case()
        )
        self.server.override_dependency(
            IGetOrdersByUserUseCase,
            self.order_container.get_orders_by_user_use_case(),
        )

    def register_routers(self) -> None:
        self.server.register_router(order_router, prefix=self.prefix, tags=self.tags)
