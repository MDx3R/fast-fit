from uuid import UUID

from common.infrastructure.database.sqlalchemy.executor import QueryExecutor
from fastfit.order.application.interfaces.repositories.order_read_repository import (
    IOrderReadRepository,
)
from fastfit.order.application.read_models.order_read_model import (
    OrderItemReadModel,
    OrderReadModel,
)
from fastfit.order.domain.value_objects.order_status import OrderStatus
from fastfit.order.infrastructure.database.postgres.sqlalchemy.models.order_base import (
    OrderBase,
)
from sqlalchemy import select


class OrderReadRepository(IOrderReadRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, order_id: UUID) -> OrderReadModel:
        stmt = select(OrderBase).where(OrderBase.order_id == order_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Order with id {order_id} not found")
        return self._to_read_model(model)

    async def get_by_user(self, user_id: UUID) -> list[OrderReadModel]:
        stmt = select(OrderBase).where(OrderBase.user_id == user_id)
        models = await self.executor.execute_scalar_many(stmt)
        return [self._to_read_model(model) for model in models]

    async def get_by_restaurant(
        self, restaurant_id: UUID, status: OrderStatus | None
    ) -> list[OrderReadModel]:
        stmt = select(OrderBase).where(OrderBase.restaurant_id == restaurant_id)
        if status:
            stmt = stmt.where(OrderBase.status == status)
        models = await self.executor.execute_scalar_many(stmt)
        return [self._to_read_model(model) for model in models]

    def _to_read_model(self, model: OrderBase) -> OrderReadModel:
        items = [
            OrderItemReadModel(
                dish_id=item.dish_id,
                quantity=item.quantity,
                price=item.price,
                currency=item.currency,
            )
            for item in model.items
        ]
        return OrderReadModel(
            order_id=model.order_id,
            user_id=model.user_id,
            phone_number=model.phone_number,
            items=items,
            total_price=model.total_price,
            currency=model.currency,
            status=model.status,
            delivery_type=model.delivery_type,
            delivery_address=model.delivery_address,
            restaurant_id=model.restaurant_id,
            created_at=model.created_at,
        )
