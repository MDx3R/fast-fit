from fastfit.menu.domain.entities.category import Category
from fastfit.menu.domain.value_objects.category_name import CategoryName
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.models.models import (
    CategoryBase,
)


class CategoryMapper:
    @staticmethod
    def to_domain(model: CategoryBase) -> Category:
        return Category(
            category_id=model.category_id,
            name=CategoryName(model.name),
            restaurant_id=model.restaurant_id,
        )

    @staticmethod
    def to_persistance(entity: Category) -> CategoryBase:
        return CategoryBase(
            category_id=entity.category_id,
            name=entity.name.value,
            restaurant_id=entity.restaurant_id,
        )
