from uuid import UUID

from fastfit.menu.application.dtos.commands.create_dish_command import CreateDishCommand
from fastfit.menu.application.interfaces.repositories.dish_repository import (
    IDishRepository,
)
from fastfit.menu.application.interfaces.usecases.command.create_dish_use_case import (
    ICreateDishUseCase,
)
from fastfit.menu.domain.interfaces.dish_factory import DishFactoryDTO, IDishFactory


class CreateDishUseCase(ICreateDishUseCase):
    def __init__(
        self, dish_factory: IDishFactory, dish_repository: IDishRepository
    ) -> None:
        self.dish_factory = dish_factory
        self.dish_repository = dish_repository

    async def execute(self, command: CreateDishCommand) -> UUID:
        dish = self.dish_factory.create(
            DishFactoryDTO(
                name=command.name,
                description=command.description,
                currency=command.currency,
                price=command.price,
                calories=command.calories,
                proteins=command.proteins,
                fats=command.fats,
                carbohydrates=command.carbohydrates,
                ingredients=command.ingredients,
                filters=command.filters,
                category_id=command.category_id,
                restaurant_id=command.restaurant_id,
                image=command.image,
            )
        )
        await self.dish_repository.add(dish)
        return dish.dish_id
