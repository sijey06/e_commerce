from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from core.database import Base
from core.status import Status

# Промежуточная таблица для связи многих-заказов и многих-продуктов
order_product_association = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

# Ассоциативная таблица для связи товаров и категорий
product_category_association = Table(
    'product_category',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Category(Base):
    """Модель категории товара."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    products = relationship("Product", secondary=product_category_association,
                            back_populates="categories")


class Product(Base):
    """Модель продукта."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    categories = relationship("Category",
                              secondary=product_category_association,
                              back_populates="products")
    orders = relationship("Order", secondary=order_product_association,
                          back_populates="ordered_products")


class CartItem(Base):
    """Модель корзины."""

    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Float, nullable=True)

    user = relationship("User", back_populates="user_cart_items")
    product = relationship("Product")


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=True)
    chat_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    user_cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Order(Base):
    """Модель заказа."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="enum_status", native_enum=True),
        nullable=False, default=Status.NEW)

    ordered_products = relationship("Product",
                                    secondary=order_product_association,
                                    back_populates="orders")
    user = relationship("User", back_populates="orders")
