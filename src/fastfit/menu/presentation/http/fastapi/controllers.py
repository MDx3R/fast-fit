import json
from typing import Annotated
from urllib.parse import quote, unquote
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastfit.identity.presentation.http.fastapi.auth import get_access_token
from fastfit.menu.application.dtos.queries.get_dish_by_id_query import GetDishByIdQuery
from fastfit.menu.application.dtos.queries.get_dishes_by_restaurant_query import (
    GetDishesByRestaurantQuery,
)
from fastfit.menu.application.interfaces.usecases.query.get_dish_by_id_use_case import (
    IGetDishByIdUseCase,
)
from fastfit.menu.application.interfaces.usecases.query.get_dishes_by_restaurant_use_case import (
    IGetDishesByRestaurantUseCase,
)
from fastfit.menu.application.read_models.dish_read_model import DishReadModel


menu_router = APIRouter()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

DEFAULT_RESTAURANT_ID: UUID = UUID(int=0)


# GET endpoint to render the menu page
@menu_router.get("/menu", name="menu")
async def get_menu(
    request: Request,
    dishes_use_case: Annotated[IGetDishesByRestaurantUseCase, Depends()],
    restaurant_id: UUID = DEFAULT_RESTAURANT_ID,  # Assume restaurant_id is passed as a query parameter
) -> HTMLResponse:
    try:
        # Fetch dishes for the given restaurant
        query = GetDishesByRestaurantQuery(restaurant_id=restaurant_id)
        dishes: list[DishReadModel] = await dishes_use_case.execute(query)

        # Extract unique categories from dishes
        categories = [
            {"id": str(dish.category.category_id), "name": dish.category.name}
            for dish in sorted(dishes, key=lambda x: x.category.name)
        ]
        # Remove duplicates while preserving order
        seen: set[str] = set()

        unique_categories: list[dict[str, str]] = []
        for cat in categories:
            if (cat["id"]) not in seen:
                seen.add(cat["id"])
                unique_categories.append(cat)

        # Prepare menu items for the template
        menu_items = [
            {
                "id": str(dish.dish_id),
                "name": dish.name,
                "description": dish.description,
                "price": f"{dish.price:.2f}",
                "calories": f"{dish.calories:.0f}",
                "category": str(dish.category.category_id),
                "proteins": f"{dish.proteins:.0f}",
                "fats": f"{dish.fats:.0f}",
                "carbohydrates": f"{dish.carbohydrates:.0f}",
                "image": dish.image or "https://placehold.co/400",  # Fallback image
            }
            for dish in dishes
        ]

        # Define calorie filter options
        calorie_options = [
            {"value": "all", "label": "Все"},  # noqa: RUF001
            {"value": "0-300", "label": "0-300 ккал"},
            {"value": "300-600", "label": "300-600 ккал"},
            {"value": "600-1000", "label": "600-1000 ккал"},
            {"value": "1000", "label": "1000+ ккал"},
        ]

        return templates.TemplateResponse(
            "menu.html",
            {
                "request": request,
                "banner_title": "Здоровая еда с FastFit",  # noqa: RUF001
                "banner_subtitle": "Вкусные и полезные блюда с доставкой или самовывозом",  # noqa: RUF001
                "banner_image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=1200",
                "categories": [
                    {"id": "all", "name": "Все"},  # noqa: RUF001
                    *unique_categories,
                ],
                "menu_items": menu_items,
                "calorie_options": calorie_options,
                "success_message": unquote(
                    request.cookies.get("success_message") or ""
                ),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching menu: {e!s}"
        ) from e


@menu_router.get("/cart", name="cart")
async def get_cart(
    request: Request, token: Annotated[str | None, Depends(get_access_token)]
) -> Response:
    if not token:
        return RedirectResponse(url="/auth/login", status_code=303)

    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "delivery_methods": [
                {"id": "delivery", "name": "Доставка"},
                {"id": "pickup", "name": "Самовывоз"},
            ],
            "payment_methods": [
                {"id": "card", "name": "Картой"},
                {"id": "cash", "name": "Наличными"},
            ],
            "restaurants": [
                {"id": None, "name": "FastFit Москва"},
                {"id": None, "name": "FastFit Санкт-Петербург"},
            ],
            "user_address": "",  # Replace with actual user address if authenticated
        },
    )


# POST endpoint to add an item to the cart
@menu_router.post("/cart/add")
async def add_to_cart(
    request: Request,
    dish_use_case: Annotated[IGetDishByIdUseCase, Depends()],
    dish_id: Annotated[UUID, Form()],
    quantity: Annotated[int, Form()] = 1,
) -> RedirectResponse:
    try:
        if quantity < 1:
            raise HTTPException(status_code=400, detail="Quantity must be at least 1")

        # Fetch dish details
        query = GetDishByIdQuery(dish_id=dish_id)
        dish: DishReadModel = await dish_use_case.execute(query)

        # Retrieve or initialize cart from session (stored in cookies)
        cart = json.loads(unquote(request.cookies.get("cart", "[]")))

        # Check if dish is already in cart
        for item in cart:
            if item["dish_id"] == str(dish.dish_id):
                item["quantity"] += quantity
                break
        else:
            # Add new item to cart
            cart.append(
                {
                    "dish_id": str(dish.dish_id),
                    "name": dish.name,
                    "price": float(dish.price),
                    "calories": float(dish.calories),
                    "protein": float(dish.proteins),
                    "fat": float(dish.fats),
                    "carbs": float(dish.carbohydrates),
                    "image": dish.image or "https://via.placeholder.com/150",
                    "quantity": quantity,
                }
            )

        # Update cart in cookies
        response = RedirectResponse(url="/menu", status_code=303)
        response.set_cookie(
            key="cart", value=quote(json.dumps(cart, ensure_ascii=False)), httponly=True
        )
        response.set_cookie(
            key="success_message",
            value=quote(f"Добавили {dish.name} в корзину!"),
            max_age=5,
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error adding to cart: {e!s}"
        ) from e
