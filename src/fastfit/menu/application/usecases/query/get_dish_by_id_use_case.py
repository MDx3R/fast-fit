from fastfit.menu.application.dtos.queries.get_dish_by_id_query import GetDishByIdQuery
from fastfit.menu.application.interfaces.repositories.dish_read_repository import (
    IDishReadRepository,
)
from fastfit.menu.application.interfaces.usecases.query.get_dish_by_id_use_case import (
    IGetDishByIdUseCase,
)
from fastfit.menu.application.read_models.dish_read_model import DishReadModel


class GetDishByIdUseCase(IGetDishByIdUseCase):
    def __init__(self, dish_read_repository: IDishReadRepository) -> None:
        self.dish_read_repository = dish_read_repository

    async def execute(self, query: GetDishByIdQuery) -> DishReadModel:
        return await self.dish_read_repository.get_by_id(query.dish_id)
