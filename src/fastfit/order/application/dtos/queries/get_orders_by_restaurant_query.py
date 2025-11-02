from dataclasses import dataclass
from uuid import UUID

from fastfit.order.domain.value_objects.order_status import OrderStatus


@dataclass
class GetOrdersByRestaurantQuery:
    restaurant_id: UUID
    status: OrderStatus | None = None
