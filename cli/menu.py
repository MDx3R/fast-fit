import asyncio
from decimal import Decimal
from typing import Any

from bootstrap.config import AppConfig
from bootstrap.utils import log_config
from common.infrastructure.database.sqlalchemy.database import Database
from common.infrastructure.di.container.container import CommonContainer
from common.infrastructure.logger.logging.logger_factory import LoggerFactory
from fastfit.menu.domain.entities.category import Category
from fastfit.menu.domain.interfaces.category_factory import CategoryFactoryDTO
from fastfit.menu.domain.interfaces.dish_factory import DishFactoryDTO
from fastfit.menu.domain.value_objects.dish_filters import DishFilterType
from fastfit.menu.infrastructure.di.container.container import (
    CategoryContainer,
    DishContainer,
)
from fastfit.menu.presentation.http.fastapi.controllers import DEFAULT_RESTAURANT_ID


async def seed_menu() -> None:
    # Загрузка конфига
    config = AppConfig.load()

    logger = LoggerFactory.create(None, config.env, config.logger)
    logger.info("logger initialized")

    log_config(logger, config)

    # Database
    logger.info("initializing database...")
    database = Database.create(config.db, logger)
    logger.info("database initialized")

    common_container = CommonContainer(config=config, database=database)
    uuid_generator = common_container.uuid_generator
    query_executor = common_container.query_executor
    uow = common_container.unit_of_work()

    category_container = CategoryContainer(
        query_executor=query_executor, uuid_generator=uuid_generator
    )
    category_factory = category_container.category_factory()
    category_repo = category_container.category_repository()

    dish_container = DishContainer(
        query_executor=query_executor, uuid_generator=uuid_generator
    )
    dish_factory = dish_container.dish_factory()
    dish_repo = dish_container.dish_repository()

    restaurant_id = DEFAULT_RESTAURANT_ID

    # Категории
    categories_data: list[dict[str, Any]] = [
        {"name": "Салаты", "restaurant_id": restaurant_id},
        {"name": "Смузи", "restaurant_id": restaurant_id},
        {"name": "Спорт-меню", "restaurant_id": restaurant_id},
    ]
    categories: list[Category] = []
    async with uow.get_session():
        for cat_data in categories_data:
            cat_dto = CategoryFactoryDTO(**cat_data)
            category = category_factory.create(cat_dto)
            await category_repo.add(category)
            categories.append(category)
        await uow.commit()

    # Блюда
    dishes_data: list[dict[str, Any]] = [
        {
            "name": "Цезарь",
            "description": "Классический салат с курицей и соусом Цезарь",  # noqa: RUF001
            "price": Decimal("350"),
            "currency": "RUB",
            "calories": Decimal("250"),
            "proteins": Decimal("20"),
            "fats": Decimal("15"),
            "carbohydrates": Decimal("10"),
            "ingredients": ["Курица", "Салат", "Сыр", "Соус"],  # noqa: RUF001
            "filters": [DishFilterType.VEGAN],
            "category_id": categories[0].category_id,
            "restaurant_id": restaurant_id,
        },
        {
            "name": "Ягодный смузи",
            "description": "Смузи из свежих ягод и банана",
            "price": Decimal("220"),
            "currency": "RUB",
            "calories": Decimal("150"),
            "proteins": Decimal("3"),
            "fats": Decimal("1"),
            "carbohydrates": Decimal("35"),
            "ingredients": ["Банан", "Ягоды", "Сок"],
            "filters": [DishFilterType.GLUTEN_FREE],
            "category_id": categories[1].category_id,
            "restaurant_id": restaurant_id,
        },
        {
            "name": "Протеиновый батончик",
            "description": "Батончик для спортсменов",
            "price": Decimal("120"),
            "currency": "RUB",
            "calories": Decimal("200"),
            "proteins": Decimal("15"),
            "fats": Decimal("5"),
            "carbohydrates": Decimal("20"),
            "ingredients": ["Протеин", "Орехи", "Мёд"],
            "filters": [DishFilterType.SPORTS_MENU],
            "category_id": categories[2].category_id,
            "restaurant_id": restaurant_id,
        },
    ]
    async with uow:
        for dish_data in dishes_data:
            dish_dto = DishFactoryDTO(**dish_data)
            dish = dish_factory.create(dish_dto)
            await dish_repo.add(dish)


if __name__ == "__main__":
    asyncio.run(seed_menu())
