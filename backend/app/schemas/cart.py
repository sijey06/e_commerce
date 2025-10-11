from typing import List, Optional

from pydantic import BaseModel

from schemas.category import CategoryResponseList


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    chat_id: int


class ProductInfo(BaseModel):
    id: int
    name: str
    description: str
    price: int
    category: CategoryResponseList
    photo_url: Optional[str]

    class Config:
        from_attributes = True


class CartItemResponse(BaseModel):
    id: int
    product: ProductInfo
    quantity: int
    total_price: float

    class Config:
        from_attributes = True


class ViewCartSchema(BaseModel):
    cart_items: List[CartItemResponse]
    grand_total: float


class UpdateCartItemSchema(BaseModel):
    quantity: int
