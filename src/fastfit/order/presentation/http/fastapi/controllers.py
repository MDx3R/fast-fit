from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Annotated, Any
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastfit.identity.domain.value_objects.descriptor import IdentityDescriptor
from fastfit.identity.presentation.http.fastapi.auth import get_descriptor
from fastfit.menu.presentation.http.fastapi.controllers import DEFAULT_RESTAURANT_ID
from fastfit.order.application.dtos.commands.create_order_command import (
    CreateOrderCommand,
    OrderItemDTO,
)
from fastfit.order.application.dtos.queries.get_order_by_id_query import (
    GetOrderByIdQuery,
)
from fastfit.order.application.dtos.queries.get_orders_by_user_query import (
    GetOrdersByUserQuery,
)
from fastfit.order.application.interfaces.usecases.command.create_order_use_case import (
    ICreateOrderUseCase,
)
from fastfit.order.application.interfaces.usecases.query.get_order_by_id_use_case import (
    IGetOrderByIdUseCase,
)
from fastfit.order.application.interfaces.usecases.query.get_orders_by_user_use_case import (
    IGetOrdersByUserUseCase,
)
from fastfit.order.application.read_models.order_read_model import OrderReadModel
from fastfit.order.domain.value_objects.delivery_type import DeliveryType
from pydantic import BaseModel


order_router = APIRouter()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")


# GET endpoint to render the profile page
@order_router.get("/profile", name="profile")
async def get_profile(
    request: Request,
    user: Annotated[IdentityDescriptor, Depends(get_descriptor)],
    orders_use_case: Annotated[IGetOrdersByUserUseCase, Depends()],
) -> HTMLResponse:
    try:
        # Fetch orders for the user
        query = GetOrdersByUserQuery(user_id=user.identity_id)
        orders: list[OrderReadModel] = await orders_use_case.execute(query)

        # Format orders for template
        formatted_orders: list[dict[str, Any]] = [
            {
                "id": str(order.order_id),
                "date": order.created_at.astimezone(ZoneInfo("Europe/Moscow")),
                "units": [
                    {
                        "quantity": item.quantity,
                        "dish": {
                            "name": item.dish.name,
                            "calories": float(item.dish.calories),
                            "proteins": float(item.dish.proteins),
                            "fats": float(item.dish.fats),
                            "carbohydrates": float(item.dish.carbohydrates),
                            "image": item.dish.image or "https://placehold.co/400",
                        },
                        "price": float(item.price),
                    }
                    for item in order.items
                ],
                "total": f"{order.total_price:.2f}",
                "status": order.status.value,
                "status_color": {
                    "created": "bg-gray-500",
                    "preparing": "bg-yellow-500",
                    "ready": "bg-green-500",
                    "delivered": "bg-blue-500",
                    "picked_up": "bg-blue-500",
                    "cancelled": "bg-red-500",
                }.get(order.status.value, "bg-gray-500"),
            }
            for order in orders
        ]

        # Generate activity calendar for the last 7 days
        today = datetime.now(UTC).astimezone(ZoneInfo("Europe/Moscow")).date()
        activity: list[dict[str, Any]] = []
        for i in range(7):
            date = today - timedelta(days=i)
            orders_on_date = [
                order
                for order in orders
                if order.created_at.astimezone(ZoneInfo("Europe/Moscow")).date() == date
            ]
            orders_count = len(orders_on_date)
            level = min(orders_count, 4)  # Levels: 0 (none), 1, 2, 3, 4 (3+ orders)
            activity.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "orders_count": orders_count,
                    "level": level,
                }
            )

        return templates.TemplateResponse(
            "profile.html",
            {
                "request": request,
                "orders": formatted_orders,
                "activity": activity[::-1],  # Reverse to show oldest to newest
                "city": "Москва",  # Replace with actual user city if available
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching profile: {e!s}"
        ) from e


@order_router.get("/orders/{order_id}", name="order_details")
async def get_order_details(
    request: Request,
    order_id: UUID,
    user: Annotated[IdentityDescriptor, Depends(get_descriptor)],
    order_use_case: Annotated[IGetOrderByIdUseCase, Depends()],
) -> HTMLResponse:
    try:
        query = GetOrderByIdQuery(order_id=order_id)
        order: OrderReadModel = await order_use_case.execute(query)
        if order.user_id != user.identity_id:
            raise HTTPException(status_code=403, detail="Access denied")
        formatted_order: dict[str, Any] = {
            "id": str(order.order_id)[:5],
            "date": order.created_at.astimezone(ZoneInfo("Europe/Moscow")),
            "units": [
                {
                    "quantity": item.quantity,
                    "dish": {
                        "name": item.dish.name,
                        "calories": float(item.dish.calories),
                        "proteins": float(item.dish.proteins),
                        "fats": float(item.dish.fats),
                        "carbohydrates": float(item.dish.carbohydrates),
                        "image": item.dish.image or "https://placehold.co/400",
                    },
                    "price": float(item.price),
                }
                for item in order.items
            ],
            "total": f"{order.total_price:.2f}",
            "status": order.status.value.capitalize(),
            "status_color": {
                "created": "bg-gray-500",
                "preparing": "bg-yellow-500",
                "ready": "bg-green-500",
                "delivered": "bg-blue-500",
                "picked_up": "bg-blue-500",
                "cancelled": "bg-red-500",
            }.get(order.status.value, "bg-gray-500"),
            "delivery_type": order.delivery_type.value,
            "delivery_address": order.delivery_address or "Самовывоз",
        }
        return templates.TemplateResponse(
            "order_details.html", {"request": request, "order": formatted_order}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Order not found: {e!s}") from e


class CreateOrderRequest(BaseModel):
    items: list[dict[str, Any]]
    delivery_type: DeliveryType
    delivery_address: str | None = None
    payment_method: str  # "card" or "cash"


# POST endpoint to create an order
@order_router.post("/orders")
async def create_order(
    order_data: CreateOrderRequest,
    user: Annotated[IdentityDescriptor, Depends(get_descriptor)],
    create_order_use_case: Annotated[ICreateOrderUseCase, Depends()],
) -> JSONResponse:
    try:
        # Validate and map data to CreateOrderCommand
        # Assume CreateOrderCommand structure based on OrderReadModel
        command = CreateOrderCommand(
            user_id=user.identity_id,
            phone_number=user.username,
            items=[
                OrderItemDTO(
                    dish_id=UUID(item["dish_id"]),
                    quantity=int(item["quantity"]),
                    price=Decimal(item["price"]),
                    currency="RUB",  # Assume RUB
                )
                for item in order_data.items
            ],
            delivery_type=DeliveryType(order_data.delivery_type),
            delivery_address=(
                order_data.delivery_address
                if order_data.delivery_type == DeliveryType.DELIVERY
                else None
            ),
            restaurant_id=DEFAULT_RESTAURANT_ID,
        )
        order_id: UUID = await create_order_use_case.execute(command)
        return JSONResponse(
            content={"order_id": str(order_id), "message": "Order created successfully"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creating order: {e!s}"
        ) from e
