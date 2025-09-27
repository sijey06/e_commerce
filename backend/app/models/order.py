import uuid

from sqlalchemy import Integer, BigInteger, Enum, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base
from enums.status import Status
from .associations import order_product


def generate_unique_order_number():
    return uuid.uuid4().hex[:8].upper()


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

    # Связи
    user = relationship("User", back_populates="orders")
    ordered_products = relationship("Product", secondary="order_product",
                                    back_populates="orders", lazy='selectin')
