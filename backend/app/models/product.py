from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base
from .associations import order_product, product_category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    # Связи
    categories = relationship("Category", secondary="product_category",
                              back_populates="products")
    orders = relationship("Order", secondary="order_product",
                          back_populates="ordered_products")
