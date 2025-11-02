from enum import Enum
from typing import ClassVar

from common.infrastructure.app.http_app import IHTTPApp
from common.infrastructure.server.fastapi.server import FastAPIServer
from fastfit.menu.application.interfaces.usecases.query.get_dish_by_id_use_case import (
    IGetDishByIdUseCase,
)
from fastfit.menu.application.interfaces.usecases.query.get_dishes_by_restaurant_use_case import (
    IGetDishesByRestaurantUseCase,
)
from fastfit.menu.infrastructure.di.container.container import DishContainer
from fastfit.menu.presentation.http.fastapi.controllers import menu_router


class MenuApp(IHTTPApp):
    prefix = ""
    tags: ClassVar[list[str | Enum]] = ["Menu"]

    def __init__(
        self,
        dish_container: DishContainer,
        server: FastAPIServer,
    ) -> None:
        self.dish_container = dish_container
        self.server = server

    def configure_dependencies(self) -> None:
        self.server.override_dependency(
            IGetDishByIdUseCase, self.dish_container.get_dish_by_id_use_case()
        )
        self.server.override_dependency(
            IGetDishesByRestaurantUseCase,
            self.dish_container.get_dishes_by_restaurant_use_case(),
        )

    def register_routers(self) -> None:
        self.server.register_router(menu_router, prefix=self.prefix, tags=self.tags)
