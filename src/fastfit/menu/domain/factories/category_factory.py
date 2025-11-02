from common.domain.interfaces.uuid_generator import IUUIDGenerator
from fastfit.menu.domain.entities.category import Category
from fastfit.menu.domain.interfaces.category_factory import (
    CategoryFactoryDTO,
    ICategoryFactory,
)
from fastfit.menu.domain.value_objects.category_name import CategoryName


class CategoryFactory(ICategoryFactory):
    def __init__(self, uuid_generator: IUUIDGenerator) -> None:
        self.uuid_generator = uuid_generator

    def create(self, data: CategoryFactoryDTO) -> Category:
        name = CategoryName.create(data.name)
        return Category.create(
            category_id=self.uuid_generator.create(),
            name=name,
            restaurant_id=data.restaurant_id,
        )
