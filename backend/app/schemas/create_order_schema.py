from pydantic import Field

from .order import OrderCreate


class CreateOrderSchema(OrderCreate):
    first_name: str
    address: str
    phone_number: str = Field(max_length=11, min_length=11)
    chat_id: int
