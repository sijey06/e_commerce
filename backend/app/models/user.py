from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=True)
    chat_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    # Связи с другими моделями
    user_cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")
