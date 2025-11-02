from uuid import UUID, uuid4

from common.domain.interfaces.clock import IClock
from common.domain.value_objects.phone_number import PhoneNumber
from fastfit.menu.domain.value_objects.money import Money
from fastfit.order.application.dtos.commands.create_order_command import (
    CreateOrderCommand,
)
from fastfit.order.application.interfaces.repositories.order_repository import (
    IOrderRepository,
)
from fastfit.order.application.interfaces.usecases.command.create_order_use_case import (
    ICreateOrderUseCase,
)
from fastfit.order.domain.entities.order import Order
from fastfit.order.domain.entities.order_item import OrderItem
from fastfit.order.domain.value_objects.delivery_address import DeliveryAddress


class CreateOrderUseCase(ICreateOrderUseCase):
    def __init__(self, clock: IClock, order_repository: IOrderRepository) -> None:
        self.clock = clock
        self.order_repository = order_repository

    async def execute(self, command: CreateOrderCommand) -> UUID:
        items = [
            OrderItem.create(
                dish_id=item.dish_id,
                quantity=item.quantity,
                price=Money.create(item.price, item.currency),
            )
            for item in command.items
        ]
        order = Order.create(
            order_id=uuid4(),
            user_id=command.user_id,
            phone_number=PhoneNumber(command.phone_number),
            items=items,
            delivery_type=command.delivery_type,
            delivery_address=(
                DeliveryAddress(command.delivery_address)
                if command.delivery_address
                else None
            ),
            restaurant_id=command.restaurant_id,
            created_at=self.clock.now(),
        )
        await self.order_repository.add(order)
        return order.order_id
