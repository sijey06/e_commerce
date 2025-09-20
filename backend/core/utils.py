from typing import Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.models import CartItem, Category, Product, User


def get_category(category_id: int, db: Session):
    """Получить категорию по id."""
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


def get_product(product_id: int, db: Session):
    """Получить продукт по id."""
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


def get_cart_item(item_id: int, user_id: int, db: Session):
    """Получить элемент корзины по id и пользователю."""
    item = db.query(CartItem).filter(CartItem.id == item_id,
                                     CartItem.user_id == user_id).first()
    if not item:
        raise HTTPException(status_code=404,
                            detail="Элемент корзины не найден")
    return item


def get_user(chat_id: Union[int, str], db: Session):
    """Получение пользователя по chat_id."""
    user = db.query(User).filter(User.chat_id == chat_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


def calculate_and_update_cart_item(existing_item: CartItem,
                                   product: Product, additional_quantity: int):
    """Рассчет количества и общей стоимости товара в корзине."""
    existing_item.quantity += additional_quantity
    existing_item.total_price = product.price * existing_item.quantity
