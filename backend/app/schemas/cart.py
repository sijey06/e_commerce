from pydantic import BaseModel
from typing import List


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    chat_id: int


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float

    class Config:
        from_attributes = True


class ViewCartSchema(BaseModel):
    cart_items: List[CartItemResponse]
    grand_total: float


class UpdateCartItemSchema(BaseModel):
    quantity: int
