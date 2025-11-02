from abc import ABC, abstractmethod

from fastfit.menu.application.dtos.queries.get_dishes_by_restaurant_query import (
    GetDishesByRestaurantQuery,
)
from fastfit.menu.application.read_models.dish_read_model import DishReadModel


class IGetDishesByRestaurantUseCase(ABC):
    @abstractmethod
    async def execute(
        self, query: GetDishesByRestaurantQuery
    ) -> list[DishReadModel]: ...
