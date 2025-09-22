from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base
from .associations import product_category


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Связь с товарами
    products = relationship("Product", secondary="product_category",
                            back_populates="categories")
