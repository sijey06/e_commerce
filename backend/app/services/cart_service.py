from typing import Any, Dict

from fastapi import HTTPException

from repositories.cart_repository import CartRepository
from schemas.cart import (CartItemCreate, CartItemResponse,
                          UpdateCartItemSchema, ViewCartSchema)


class CartService:
    """Класс для обслуживания операций с корзиной."""

    @staticmethod
    async def add_to_cart(cart_item: CartItemCreate, db_session):
        """
        Добавляет товар в корзину.

        Параметры:
        - cart_item (CartItemCreate): Данные для добавления товара в корзину.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Объект модели результата добавления товара.
        """
        repo = CartRepository(db_session)
        try:
            created_cartitem = await repo.add_to_cart(cart_item)
            return CartItemResponse.model_validate(
                created_cartitem).model_dump()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def view_cart(chat_id: int, db_session) -> ViewCartSchema:
        """
        Отображает содержимое корзины пользователя.

        Параметры:
        - chat_id (int): Чат-идентификатор пользователя.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Содержимое корзины пользователя.
        """
        repo = CartRepository(db_session)
        try:
            items = await repo.get_cart_items_by_user_id(chat_id)
            cart_items = [
                CartItemResponse.model_validate(item) for item in items
            ]
            grand_total = sum(item.total_price for item in items)
            return ViewCartSchema(cart_items=cart_items,
                                  grand_total=grand_total)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def update_cart_item(chat_id: int, item_id: int,
                               data: UpdateCartItemSchema,
                               db_session) -> Dict[str, Any]:
        """
        Обновляет выбранный элемент в корзине.

        Параметры:
        - chat_id (int): Чат-идентификатор пользователя.
        - item_id (int): Идентификатор элемента в корзине.
        - data (UpdateCartItemSchema): Данные для обновления.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Результат операции и статус.
        """
        repo = CartRepository(db_session)
        try:
            updated_item = await repo.update_cart_item(chat_id, item_id, data)
            return {"message": "Элемент корзины успешно обновлен.",
                    "data": updated_item}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def remove_from_cart(chat_id: int, item_id: int,
                               db_session) -> Dict[str, Any]:
        """
        Удаляет указанный элемент из корзины пользователя.

        Параметры:
        - chat_id (int): Чат-идентификатор пользователя.
        - item_id (int): Идентификатор элемента в корзине.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Результат операции и статус.
        """
        repo = CartRepository(db_session)
        try:
            await repo.remove_from_cart(chat_id, item_id)
            return {"message": "Элемент успешно удалён из корзины."}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
