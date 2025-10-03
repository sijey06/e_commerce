from database import Base
from sqlalchemy import BigInteger, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[int] = mapped_column(BigInteger, nullable=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True,
                                         nullable=False)

    # Связи с другими моделями
    user_cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")
