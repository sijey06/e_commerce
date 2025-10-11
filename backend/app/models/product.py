from typing import TYPE_CHECKING

from database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import order_product

if TYPE_CHECKING:
    from models.category import Category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    # Связи с другими моделями
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(
        back_populates="products", lazy="joined")
    orders = relationship("Order", secondary="order_product",
                          back_populates="ordered_products", lazy="selectin")

    def __str__(self):
        return self.name
