from sqlalchemy import (BigInteger, Enum, ForeignKey,
                        Integer, String, select, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property

from database import Base
from enums.status import Status
from .associations import order_product
from models.product import Product
from utils.generate_id import generate_unique_order_number


def calculate_total_amount_expression():
    """Возвращает SQL-выражение для вычисления общей суммы заказа."""
    return select(
        func.coalesce(
            select(func.sum(Product.price))
            .select_from(order_product.join(Product))
            .where(order_product.c.order_id == Order.id)
            .correlate_except(Product)
            .scalar_subquery(),
            0
        )
    ).scalar_subquery()


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    number: Mapped[str] = mapped_column(String, unique=True,
                                        nullable=False,
                                        default=generate_unique_order_number)
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="enum_status", native_enum=True),
        nullable=False, default=Status.NEW)
    total_amount = column_property(select(func.coalesce(
        select(func.sum(Product.price))
        .select_from(order_product.join(Product))
        .where(order_product.c.order_id == id)
        .correlate_except(Product)
        .scalar_subquery(),
        0
        )
    ).scalar_subquery())

    # Связи с другими моделями
    user = relationship("User", back_populates="orders")
    ordered_products = relationship("Product", secondary="order_product",
                                    back_populates="orders", lazy='selectin')
