from pydantic import BaseModel
from typing import List
from .product import ProductResponse
from .status import Status


class OrderCreate(BaseModel):
    user_id: int
    status: Status = Status.NEW


class OrderResponse(OrderCreate):
    id: int
    ordered_products: List[ProductResponse]

    class Config:
        from_attributes = True
