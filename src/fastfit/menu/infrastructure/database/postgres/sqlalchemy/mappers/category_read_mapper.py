from fastfit.menu.application.read_models.category_read_model import CategoryReadModel
from fastfit.menu.infrastructure.database.postgres.sqlalchemy.models.models import (
    CategoryBase,
)


class CategoryReadMapper:
    @staticmethod
    def to_read_model(model: CategoryBase) -> CategoryReadModel:
        return CategoryReadModel(
            category_id=model.category_id,
            name=model.name,
            restaurant_id=model.restaurant_id,
        )
