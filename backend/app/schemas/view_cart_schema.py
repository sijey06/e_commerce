from pydantic import BaseModel
from typing import List
from .product import ProductResponse


class ViewCartItemSchema(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    product: ProductResponse

    class Config:
        from_attributes = True


class ViewCartSchema(BaseModel):
    cart_items: List[ViewCartItemSchema]
    grand_total: float
