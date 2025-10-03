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


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    photo_url: Optional[str] = None
