from typing import List, Optional

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """Схема возвращения пользователя."""

    id: int
    first_name: str
    address: str
    phone_number: int
    chat_id: int

    model_config = {
        "from_attributes": True
    }


class CategoryCreate(BaseModel):
    """Создание новой категории."""

    name: str


class CategoryResponse(CategoryCreate):
    """Описание возвращённой категории."""

    id: int

    model_config = {
        "from_attributes": True
    }


class ProductCreate(BaseModel):
    """Создание нового продукта."""

    name: str
    description: str
    price: float
    photo_url: Optional[str]

    model_config = {
        "from_attributes": True
    }


class ProductResponse(ProductCreate):
    """Описание возвращаемого продукта."""

    id: int
    name: str
    description: str
    price: float
    photo_url: Optional[str]
    categories: List[CategoryResponse]

    model_config = {
        "from_attributes": True
    }


class AddToCartSchema(BaseModel):
    """Добавление товара в корзину."""

    product_id: int
    quantity: int = 1
    chat_id: int


class UpdateCartItemSchema(BaseModel):
    """Изменение количества товара в корзине."""

    quantity: int


class ViewCartItemSchema(BaseModel):
    """Представление элемента корзины."""

    id: int
    product_id: int
    quantity: int
    total_price: float

    model_config = {
        "from_attributes": True
    }


class ViewCartSchema(BaseModel):
    """Представление корзины покупателя."""

    cart_items: List[ViewCartItemSchema]
    grand_total: float

    model_config = {
        "from_attributes": True
    }


class OrderStatusCreate(BaseModel):
    """Изменение статуса заказа."""

    status: str


class OrderStatusResponse(OrderStatusCreate):
    """Возвращаемый объект статуса заказа."""

    id: int

    model_config = {
        "from_attributes": True
    }


class CreateOrderSchema(BaseModel):
    """Данные для создания заказа."""

    first_name: str
    address: str
    phone_number: str = Field(max_length=11, min_length=11)
    chat_id: int


class OrderResponse(BaseModel):
    """Схема возвращения полного заказа."""

    id: int
    status: str
    products: List[ProductResponse]

    model_config = {
        "from_attributes": True
    }
