from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from schemas.category import CategoryResponseList


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    photo_url: Optional[str]


class ProductResponse(ProductCreate):
    id: int
    name: str
    description: str
    price: int
    category: "CategoryResponseList"
    photo_url: Optional[str]

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    photo_url: Optional[str] = None
