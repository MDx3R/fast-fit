from typing import Any

from dependency_injector import containers, providers
from fastfit.menu.application.usecases.query.get_dish_by_id_use_case import (
    GetDishByIdUseCase,
)
from fastfit.menu.application.usecases.query.get_dishes_by_restaurant_use_case import (
    GetDishesByRestaurantUseCase,
)
from fastfit.menu.domain.factories.category_factory import CategoryFactory
from fastfit.menu.domain.factories.dish_factory import DishFactory
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.repositories.category_repository import (
    CategoryRepository,
)
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.repositories.dish_read_repository import (
    DishReadRepository,
)
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.repositories.dish_repository import (
    DishRepository,
)


class CategoryContainer(containers.DeclarativeContainer):
    query_executor: providers.Dependency[Any] = providers.Dependency()
    uuid_generator: providers.Dependency[Any] = providers.Dependency()

    category_factory = providers.Singleton(CategoryFactory, uuid_generator)

    category_repository = providers.Singleton(CategoryRepository, query_executor)


class DishContainer(containers.DeclarativeContainer):
    query_executor: providers.Dependency[Any] = providers.Dependency()
    uuid_generator: providers.Dependency[Any] = providers.Dependency()

    dish_factory = providers.Singleton(DishFactory, uuid_generator)

    dish_repository = providers.Singleton(DishRepository, query_executor)
    dish_read_repository = providers.Singleton(DishReadRepository, query_executor)

    get_dish_by_id_use_case = providers.Singleton(
        GetDishByIdUseCase, dish_read_repository=dish_read_repository
    )
    get_dishes_by_restaurant_use_case = providers.Singleton(
        GetDishesByRestaurantUseCase,
        dish_read_repository=dish_read_repository,
    )
