from common.domain.interfaces.uuid_generator import IUUIDGenerator
from fastfit.menu.domain.entities.dish import Dish
from fastfit.menu.domain.interfaces.dish_factory import DishFactoryDTO, IDishFactory
from fastfit.menu.domain.value_objects.dish_filters import DishFilters
from fastfit.menu.domain.value_objects.dish_name import DishName
from fastfit.menu.domain.value_objects.ingredients import Ingredients
from fastfit.menu.domain.value_objects.money import Money
from fastfit.menu.domain.value_objects.nutritional_info import NutritionalInfo


class DishFactory(IDishFactory):
    def __init__(self, uuid_generator: IUUIDGenerator) -> None:
        self.uuid_generator = uuid_generator

    def create(self, data: DishFactoryDTO) -> Dish:
        name = DishName.create(data.name)
        price = Money.create(data.price, data.currency)
        nutritional_info = NutritionalInfo.create(
            data.calories, data.proteins, data.fats, data.carbohydrates
        )
        ingredients = Ingredients.create(data.ingredients)
        filters = DishFilters.create(data.filters)

        return Dish.create(
            dish_id=self.uuid_generator.create(),
            name=name,
            description=data.description,
            price=price,
            nutritional_info=nutritional_info,
            ingredients=ingredients,
            filters=filters,
            category_id=data.category_id,
            restaurant_id=data.restaurant_id,
        )
