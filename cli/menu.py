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
        {"name": "Основные блюда", "restaurant_id": restaurant_id},
        {"name": "Десерты и напитки", "restaurant_id": restaurant_id},
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
        # Салаты (Salads)
        {
            "name": "Капрезе",
            "description": "Освежающий салат с ломтиками томатов, свежей моцареллой, базиликом, бальзамическим уксусом и оливковым маслом.",
            "price": Decimal("340"),
            "currency": "RUB",
            "calories": Decimal("200"),
            "proteins": Decimal("10"),
            "fats": Decimal("15"),
            "carbohydrates": Decimal("6"),
            "ingredients": [
                "Томаты",
                "Моцарелла",
                "Базилик",
                "Бальзамический уксус",
                "Оливковое масло",
            ],
            "filters": [DishFilterType.VEGAN, DishFilterType.GLUTEN_FREE],
            "category_id": categories[0].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/9.webp",
        },
        {
            "name": "Салат с киноа и авокадо",
            "description": "Питательный салат с киноа, авокадо, черри томатами, огурцами, красным перцем и лимонной заправкой.",
            "price": Decimal("360"),
            "currency": "RUB",
            "calories": Decimal("280"),
            "proteins": Decimal("12"),
            "fats": Decimal("14"),
            "carbohydrates": Decimal("20"),
            "ingredients": [
                "Киноа",
                "Авокадо",
                "Томаты черри",
                "Огурцы",
                "Красный перец",
                "Лимонная заправка",
            ],
            "filters": [DishFilterType.VEGAN, DishFilterType.GLUTEN_FREE],
            "category_id": categories[0].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/6.webp",
        },
        {
            "name": "Томатный брускетта",
            "description": "Легкая закуска с поджаренным багетом, томатами, базиликом, чесноком и бальзамическим соусом.",
            "price": Decimal("250"),
            "currency": "RUB",
            "calories": Decimal("120"),
            "proteins": Decimal("4"),
            "fats": Decimal("5"),
            "carbohydrates": Decimal("15"),
            "ingredients": [
                "Багет",
                "Томаты",
                "Базилик",
                "Чеснок",
                "Оливковое масло",
                "Бальзамический соус",
            ],
            "filters": [DishFilterType.VEGAN],
            "category_id": categories[0].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/7.webp",
        },
        {
            "name": "Овощной салат с фалафелем",
            "description": "Салат с фалафелем, томатами, огурцами, красным луком, латуком и соусом тахини.",
            "price": Decimal("380"),
            "currency": "RUB",
            "calories": Decimal("400"),
            "proteins": Decimal("12"),
            "fats": Decimal("18"),
            "carbohydrates": Decimal("45"),
            "ingredients": [
                "Фалафель",
                "Томаты",
                "Огурцы",
                "Красный лук",
                "Латук",
                "Соус тахини",
            ],
            "filters": [DishFilterType.VEGAN],
            "category_id": categories[0].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/29.webp",
        },
        # Смузи (Smoothies)
        {
            "name": "Манговый ласси",
            "description": "Освежающий напиток из спелого манго, йогурта, молока и щепотки кардамона.",
            "price": Decimal("220"),
            "currency": "RUB",
            "calories": Decimal("180"),
            "proteins": Decimal("5"),
            "fats": Decimal("3"),
            "carbohydrates": Decimal("32"),
            "ingredients": ["Манго", "Йогурт", "Молоко", "Мёд", "Кардамон"],
            "filters": [DishFilterType.GLUTEN_FREE],
            "category_id": categories[1].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/22.webp",
        },
        {
            "name": "Чернично-банановый смузи",
            "description": "Питательный смузи с черникой, бананом, греческим йогуртом и миндальным молоком.",
            "price": Decimal("230"),
            "currency": "RUB",
            "calories": Decimal("220"),
            "proteins": Decimal("8"),
            "fats": Decimal("4"),
            "carbohydrates": Decimal("35"),
            "ingredients": [
                "Черника",
                "Банан",
                "Греческий йогурт",
                "Миндальное молоко",
                "Мёд",
            ],
            "filters": [DishFilterType.GLUTEN_FREE],
            "category_id": categories[1].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/25.webp",
        },
        {
            "name": "Зеленый шпинатный смузи",
            "description": "Полезный смузи с шпинатом, бананом, яблоком и кокосовой водой для детокса.",
            "price": Decimal("240"),
            "currency": "RUB",
            "calories": Decimal("140"),
            "proteins": Decimal("4"),
            "fats": Decimal("2"),
            "carbohydrates": Decimal("30"),
            "ingredients": ["Шпинат", "Банан", "Яблоко", "Кокосовая вода"],
            "filters": [DishFilterType.VEGAN, DishFilterType.GLUTEN_FREE],
            "category_id": categories[1].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://plus.unsplash.com/premium_photo-1700084621249-b22c621ac4e9?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=721",
        },
        {
            "name": "Тропический смузи",
            "description": "Экзотический смузи с манго, ананасом и апельсиновым соком для яркого вкуса.",
            "price": Decimal("230"),
            "currency": "RUB",
            "calories": Decimal("160"),
            "proteins": Decimal("3"),
            "fats": Decimal("1"),
            "carbohydrates": Decimal("38"),
            "ingredients": ["Манго", "Ананас", "Апельсиновый сок"],
            "filters": [DishFilterType.VEGAN, DishFilterType.GLUTEN_FREE],
            "category_id": categories[1].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://images.unsplash.com/photo-1610970881699-44a5587cabec?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=687",
        },
        # Спорт-меню (Sports Menu)
        {
            "name": "Курица с манговой сальсой",
            "description": "Запеченные куриные бедра с сальсой из манго, красного лука, кинзы и лайма, подаются с рисом.",
            "price": Decimal("400"),
            "currency": "RUB",
            "calories": Decimal("380"),
            "proteins": Decimal("25"),
            "fats": Decimal("10"),
            "carbohydrates": Decimal("40"),
            "ingredients": [
                "Куриные бедра",
                "Манго",
                "Красный лук",
                "Кинза",
                "Лайм",
                "Рис",
            ],
            "filters": [DishFilterType.SPORTS_MENU, DishFilterType.GLUTEN_FREE],
            "category_id": categories[2].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/5.webp",
        },
        {
            "name": "Говядина с брокколи",
            "description": "Обжаренная говядина с брокколи в соевом соусе, подается с белым рисом.",
            "price": Decimal("450"),
            "currency": "RUB",
            "calories": Decimal("380"),
            "proteins": Decimal("30"),
            "fats": Decimal("12"),
            "carbohydrates": Decimal("35"),
            "ingredients": [
                "Говядина",
                "Брокколи",
                "Соевый соус",
                "Чеснок",
                "Имбирь",
                "Рис",
            ],
            "filters": [DishFilterType.SPORTS_MENU],
            "category_id": categories[2].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/8.webp",
        },
        {
            "name": "Креветки с пастой",
            "description": "Лингвини с креветками, чесноком, лимонным соком и белым вином для легкого ужина.",
            "price": Decimal("420"),
            "currency": "RUB",
            "calories": Decimal("400"),
            "proteins": Decimal("22"),
            "fats": Decimal("10"),
            "carbohydrates": Decimal("50"),
            "ingredients": [
                "Лингвини",
                "Креветки",
                "Чеснок",
                "Белое вино",
                "Лимонный сок",
            ],
            "filters": [DishFilterType.SPORTS_MENU],
            "category_id": categories[2].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/10.webp",
        },
        {
            "name": "Куриный бириани",
            "description": "Ароматный рис басмати с курицей, специями и свежей зеленью для сбалансированного питания.",
            "price": Decimal("480"),
            "currency": "RUB",
            "calories": Decimal("550"),
            "proteins": Decimal("28"),
            "fats": Decimal("15"),
            "carbohydrates": Decimal("60"),
            "ingredients": [
                "Рис басмати",
                "Курица",
                "Йогурт",
                "Специи",
                "Кинза",
                "Мята",
            ],
            "filters": [DishFilterType.SPORTS_MENU],
            "category_id": categories[2].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/11.webp",
        },
        # Основные блюда (Main Courses)
        {
            "name": "Марокканский тажин с нутом",
            "description": "Ароматное блюдо с нутом, томатами, морковью и специями, подается с кускусом.",
            "price": Decimal("390"),
            "currency": "RUB",
            "calories": Decimal("320"),
            "proteins": Decimal("10"),
            "fats": Decimal("8"),
            "carbohydrates": Decimal("50"),
            "ingredients": [
                "Нут",
                "Томаты",
                "Морковь",
                "Овощной бульон",
                "Оливки",
                "Кинза",
            ],
            "filters": [DishFilterType.VEGAN, DishFilterType.GLUTEN_FREE],
            "category_id": categories[3].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/17.webp",
        },
        {
            "name": "Корейский бибибап",
            "description": "Рис с говядиной булгоги, морковью, шпинатом, цукини и яйцом, приправленный соусом гочуджан.",
            "price": Decimal("500"),
            "currency": "RUB",
            "calories": Decimal("550"),
            "proteins": Decimal("25"),
            "fats": Decimal("15"),
            "carbohydrates": Decimal("60"),
            "ingredients": [
                "Рис",
                "Говядина булгоги",
                "Морковь",
                "Шпинат",
                "Цукини",
                "Яйцо",
                "Гочуджан",
            ],
            "filters": [],
            "category_id": categories[3].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/18.webp",
        },
        {
            "name": "Тайский зеленый карри",
            "description": "Курица с баклажанами и перцем в кокосовом соусе с зеленой пастой карри.",
            "price": Decimal("450"),
            "currency": "RUB",
            "calories": Decimal("480"),
            "proteins": Decimal("20"),
            "fats": Decimal("18"),
            "carbohydrates": Decimal("50"),
            "ingredients": [
                "Курица",
                "Кокосовое молоко",
                "Зеленая паста карри",
                "Баклажаны",
                "Перец",
                "Базилик",
            ],
            "filters": [DishFilterType.GLUTEN_FREE],
            "category_id": categories[3].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/21.webp",
        },
        {
            "name": "Русский борщ",
            "description": "Традиционный свекольный суп с капустой, картофелем и морковью, подается с ложкой сметаны.",
            "price": Decimal("300"),
            "currency": "RUB",
            "calories": Decimal("220"),
            "proteins": Decimal("8"),
            "fats": Decimal("6"),
            "carbohydrates": Decimal("30"),
            "ingredients": [
                "Свекла",
                "Капуста",
                "Картофель",
                "Морковь",
                "Томатная паста",
                "Бульон",
            ],
            "filters": [DishFilterType.GLUTEN_FREE],
            "category_id": categories[3].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/27.webp",
        },
        # Десерты и напитки (Desserts and Beverages)
        {
            "name": "Овсяное печенье",
            "description": "Полезное овсяное печенье с изюмом и орехами, идеально для перекуса.",
            "price": Decimal("150"),
            "currency": "RUB",
            "calories": Decimal("200"),
            "proteins": Decimal("4"),
            "fats": Decimal("10"),
            "carbohydrates": Decimal("25"),
            "ingredients": ["Овсяные хлопья", "Изюм", "Орехи", "Мёд"],
            "filters": [DishFilterType.VEGAN],
            "category_id": categories[4].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/3.webp",  # Using Chocolate Chip Cookies image as a placeholder
        },
        {
            "name": "Японский рамен",
            "description": "Легкий суп с лапшой рамен, грибами шиитаке, бок-чой и куриным бульоном.",
            "price": Decimal("400"),
            "currency": "RUB",
            "calories": Decimal("480"),
            "proteins": Decimal("20"),
            "fats": Decimal("12"),
            "carbohydrates": Decimal("60"),
            "ingredients": [
                "Лапша рамен",
                "Куриный бульон",
                "Грибы шиитаке",
                "Бок-чой",
                "Яйцо",
            ],
            "filters": [],
            "category_id": categories[3].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/16.webp",
        },
        {
            "name": "Сааг с макки ди роти",
            "description": "Традиционное блюдо из шпината и горчичной зелени с кукурузной лепешкой.",
            "price": Decimal("350"),
            "currency": "RUB",
            "calories": Decimal("280"),
            "proteins": Decimal("10"),
            "fats": Decimal("8"),
            "carbohydrates": Decimal("40"),
            "ingredients": [
                "Шпинат",
                "Горчичная зелень",
                "Кукурузная мука",
                "Лук",
                "Чеснок",
            ],
            "filters": [DishFilterType.VEGAN],
            "category_id": categories[3].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/15.webp",
        },
        {
            "name": "Южноиндийская масала доса",
            "description": "Тонкая рисовая блинная с начинкой из картофельного пюре, подается с кокосовым чатни.",
            "price": Decimal("320"),
            "currency": "RUB",
            "calories": Decimal("320"),
            "proteins": Decimal("8"),
            "fats": Decimal("10"),
            "carbohydrates": Decimal("50"),
            "ingredients": [
                "Рисовая мука",
                "Картофель",
                "Лук",
                "Куркума",
                "Кокосовый чатни",
            ],
            "filters": [DishFilterType.VEGAN],
            "category_id": categories[3].category_id,
            "restaurant_id": restaurant_id,
            "image": "https://cdn.dummyjson.com/recipe-images/28.webp",
        },
    ]
    async with uow:
        for dish_data in dishes_data:
            dish_dto = DishFactoryDTO(**dish_data)
            dish = dish_factory.create(dish_dto)
            await dish_repo.add(dish)


if __name__ == "__main__":
    asyncio.run(seed_menu())
