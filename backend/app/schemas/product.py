from pydantic import BaseModel
from typing import Optional, List

from .category import CategoryResponse


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    photo_url: Optional[str]


class ProductResponse(ProductCreate):
    id: int
    categories: List[CategoryResponse]

    class Config:
        from_attributes = True
