from decimal import Decimal
from uuid import UUID

from common.infrastructure.database.sqlalchemy.models.base import Base
from sqlalchemy import Numeric, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column


class DishBase(Base):
    __tablename__ = "dishes"

    dish_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    calories: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    proteins: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    fats: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    carbohydrates: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    ingredients: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    filters: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    category_id: Mapped[UUID] = mapped_column(PGUUID, nullable=False)
    restaurant_id: Mapped[UUID] = mapped_column(PGUUID, nullable=False)
