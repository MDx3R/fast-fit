from abc import ABC, abstractmethod

from fastfit.menu.application.dtos.queries.get_dish_by_id_query import GetDishByIdQuery
from fastfit.menu.application.read_models.dish_read_model import DishReadModel


class IGetDishByIdUseCase(ABC):
    @abstractmethod
    async def execute(self, query: GetDishByIdQuery) -> DishReadModel: ...
