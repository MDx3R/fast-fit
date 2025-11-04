from common.domain.value_objects.datetime import DateTime
from common.domain.value_objects.phone_number import PhoneNumber
from fastfit.menu.domain.value_objects.money import Money
from fastfit.order.domain.entities.order import Order
from fastfit.order.domain.entities.order_item import OrderItem
from fastfit.order.domain.value_objects.delivery_address import DeliveryAddress
from fastfit.order.infrastructure.database.postgres.sqlalchemy.models.order_base import (
    OrderBase,
    OrderItemBase,
)


class OrderMapper:
    @staticmethod
    def to_domain(model: OrderBase) -> Order:
        items = [
            OrderItem(
                dish_id=item.dish_id,
                quantity=item.quantity,
                price=Money.create(item.price, item.currency),
            )
            for item in model.items
        ]

        return Order(
            order_id=model.order_id,
            user_id=model.user_id,
            phone_number=PhoneNumber(model.phone_number),
            items=items,
            status=model.status,
            delivery_type=model.delivery_type,
            delivery_address=(
                DeliveryAddress(model.delivery_address)
                if model.delivery_address
                else None
            ),
            restaurant_id=model.restaurant_id,
            created_at=DateTime(model.created_at),
        )

    @staticmethod
    def to_persistence(entity: Order) -> OrderBase:
        items = [
            OrderItemBase(
                order_id=entity.order_id,
                dish_id=item.dish_id,
                quantity=item.quantity,
                price=item.price.amount,
                currency=item.price.currency,
            )
            for item in entity.items
        ]
        return OrderBase(
            order_id=entity.order_id,
            user_id=entity.user_id,
            phone_number=entity.phone_number.value,
            status=entity.status,
            delivery_type=entity.delivery_type,
            delivery_address=(
                entity.delivery_address.value if entity.delivery_address else None
            ),
            restaurant_id=entity.restaurant_id,
            created_at=entity.created_at.value,
            items=items,
        )
