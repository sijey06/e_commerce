from sqlalchemy import Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base
from enums.status import Status
from .associations import order_product


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="enum_status", native_enum=True),
        nullable=False, default=Status.NEW)

    # Связи
    user = relationship("User", back_populates="orders")
    ordered_products = relationship("Product", secondary="order_product",
                                    back_populates="orders")
