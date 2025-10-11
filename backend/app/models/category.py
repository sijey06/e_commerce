from typing import List, TYPE_CHECKING

from database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.product import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Связь с товарами
    products: Mapped[List[Product]] = relationship(
        back_populates="category", lazy="selectin")

    def __str__(self):
        return self.name
