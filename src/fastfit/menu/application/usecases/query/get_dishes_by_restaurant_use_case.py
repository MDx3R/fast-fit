from fastfit.menu.application.dtos.queries.get_dishes_by_restaurant_query import (
    GetDishesByRestaurantQuery,
)
from fastfit.menu.application.interfaces.repositories.dish_read_repository import (
    IDishReadRepository,
)
from fastfit.menu.application.interfaces.usecases.query.get_dishes_by_restaurant_use_case import (
    IGetDishesByRestaurantUseCase,
)
from fastfit.menu.application.read_models.dish_read_model import DishReadModel


class GetDishesByRestaurantUseCase(IGetDishesByRestaurantUseCase):
    def __init__(self, dish_read_repository: IDishReadRepository) -> None:
        self.dish_read_repository = dish_read_repository

    async def execute(self, query: GetDishesByRestaurantQuery) -> list[DishReadModel]:
        # If any filtering criteria present, use repository.filter which supports filters and max_calories
        if query.filters or query.max_calories is not None:
            filters = query.filters or []
            return await self.dish_read_repository.filter(
                query.restaurant_id, filters, query.max_calories
            )

        # Otherwise fetch all dishes for the restaurant
        return await self.dish_read_repository.get_by_restaurant(query.restaurant_id)
