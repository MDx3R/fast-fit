from enum import Enum


class OrderStatus(Enum):
    CREATED = "created"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    PICKED_UP = "picked_up"
