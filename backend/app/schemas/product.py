from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    photo_url: Optional[str]


class ProductResponse(ProductCreate):
    id: int
    name: str
    description: str
    price: float
    photo_url: Optional[str]

    class Config:
        from_attributes = True
