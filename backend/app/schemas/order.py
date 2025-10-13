from typing import List

from pydantic import BaseModel, Field

from .product import ProductResponse
from .status import Status


class OrderCreate(BaseModel):
    first_name: str
    address: str
    phone_number: str = Field(max_length=11, min_length=11)
    chat_id: int
    status: Status = Status.NEW


class OrderResponse(BaseModel):
    id: int
    user_id: int
    number: str
    status: Status
    ordered_products: List[ProductResponse]
    total_amount: int

    class Config:
        from_attributes = True
