from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Float, nullable=True)

    # Связи
    user = relationship("User", back_populates="user_cart_items")
    product = relationship("Product")
