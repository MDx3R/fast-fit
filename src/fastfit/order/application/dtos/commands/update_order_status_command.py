from dataclasses import dataclass
from uuid import UUID

from fastfit.order.domain.value_objects.order_status import OrderStatus


@dataclass
class UpdateOrderStatusCommand:
    order_id: UUID
    status: OrderStatus
