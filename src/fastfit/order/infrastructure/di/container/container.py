from typing import Any

from dependency_injector import containers, providers
from fastfit.order.application.usecases.command.create_order_use_case import (
    CreateOrderUseCase,
)
from fastfit.order.application.usecases.query.get_order_by_id_use_case import (
    GetOrderByIdUseCase,
)
from fastfit.order.application.usecases.query.get_orders_by_user_use_case import (
    GetOrdersByUserUseCase,
)
from fastfit.order.infrastructure.database.postgres.sqlalchemy.order_read_repository import (
    OrderReadRepository,
)
from fastfit.order.infrastructure.database.postgres.sqlalchemy.order_repository import (
    OrderRepository,
)


class OrderContainer(containers.DeclarativeContainer):
    query_executor: providers.Dependency[Any] = providers.Dependency()
    clock: providers.Dependency[Any] = providers.Dependency()
    uuid_generator: providers.Dependency[Any] = providers.Dependency()

    order_repository = providers.Singleton(OrderRepository, query_executor)
    order_read_repository = providers.Singleton(OrderReadRepository, query_executor)

    create_order_use_case = providers.Singleton(
        CreateOrderUseCase,
        uuid_generator=uuid_generator,
        clock=clock,
        order_repository=order_repository,
    )

    get_order_by_id_use_case = providers.Singleton(
        GetOrderByIdUseCase,
        order_read_repository=order_read_repository,
    )

    get_orders_by_user_use_case = providers.Singleton(
        GetOrdersByUserUseCase,
        order_read_repository=order_read_repository,
    )
