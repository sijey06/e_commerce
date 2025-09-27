from typing import List

from pydantic import BaseModel

from schemas.product import ProductResponse


class CategoryCreate(BaseModel):
    name: str


class CategoryResponseList(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


class CategoryResponse(CategoryCreate):
    id: int
    products: List[ProductResponse]

    class Config:
        from_attributes = True
