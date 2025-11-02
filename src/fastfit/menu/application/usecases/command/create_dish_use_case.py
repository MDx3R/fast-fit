from uuid import UUID, uuid4

from fastfit.menu.application.dtos.commands.create_dish_command import CreateDishCommand
from fastfit.menu.application.interfaces.repositories.dish_repository import (
    IDishRepository,
)
from fastfit.menu.application.interfaces.usecases.command.create_dish_use_case import (
    ICreateDishUseCase,
)
from fastfit.menu.domain.entities.dish import Dish
from fastfit.menu.domain.value_objects.dish_filters import DishFilters
from fastfit.menu.domain.value_objects.dish_name import DishName
from fastfit.menu.domain.value_objects.ingredients import Ingredients
from fastfit.menu.domain.value_objects.money import Money
from fastfit.menu.domain.value_objects.nutritional_info import NutritionalInfo


class CreateDishUseCase(ICreateDishUseCase):
    def __init__(self, dish_repository: IDishRepository) -> None:
        self.dish_repository = dish_repository

    async def execute(self, command: CreateDishCommand) -> UUID:
        dish = Dish.create(
            dish_id=uuid4(),
            name=DishName.create(command.name),
            description=command.description,
            price=Money.create(command.price, command.currency),
            nutritional_info=NutritionalInfo.create(
                command.calories, command.proteins, command.fats, command.carbohydrates
            ),
            ingredients=Ingredients.create(command.ingredients),
            filters=DishFilters.create(command.filters),
            category_id=command.category_id,
            restaurant_id=command.restaurant_id,
        )
        await self.dish_repository.add(dish)
        return dish.dish_id
