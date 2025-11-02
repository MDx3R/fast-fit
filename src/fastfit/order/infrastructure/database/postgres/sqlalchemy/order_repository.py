from uuid import UUID

from common.infrastructure.database.sqlalchemy.executor import QueryExecutor
from fastfit.order.application.interfaces.repositories.order_repository import (
    IOrderRepository,
)
from fastfit.order.domain.entities.order import Order
from fastfit.order.infrastructure.database.postgres.sqlalchemy.mappers.order_mapper import (
    OrderMapper,
)
from fastfit.order.infrastructure.database.postgres.sqlalchemy.models.order_base import (
    OrderBase,
)
from sqlalchemy import select


class OrderRepository(IOrderRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, order_id: UUID) -> Order:
        stmt = select(OrderBase).where(OrderBase.order_id == order_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Order with id {order_id} not found")
        return OrderMapper.to_domain(model)

    async def add(self, entity: Order) -> None:
        model = OrderMapper.to_persistence(entity)
        await self.executor.add(model)

    async def update(self, entity: Order) -> None:
        model = OrderMapper.to_persistence(entity)
        await self.executor.save(model)
