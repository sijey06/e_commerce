from typing import Any, Dict, List
from fastapi import HTTPException
from repositories.cart_repository import CartRepository
from schemas.cart import CartItemCreate, UpdateCartItemSchema


class CartService:
    """Класс для обслуживания операций с корзиной."""

    @staticmethod
    async def add_to_cart(cart_item: CartItemCreate,
                          db_session) -> Dict[str, Any]:
        """
        Добавляет товар в корзину.

        Параметры:
        - cart_item (CartItemCreate): Данные для добавления товара в корзину.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Словарь с результатом операции и статусом.
        """
        repo = CartRepository(db_session)
        try:
            added_item = await repo.add_to_cart(cart_item)
            return {
                "message": "Товар успешно добавлен в корзину.",
                "data": added_item
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def view_cart(chat_id: int, db_session) -> List[Dict[str, Any]]:
        """
        Отображает содержимое корзины пользователя.

        Параметры:
        - chat_id (int): Чат-идентификатор пользователя.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Список элементов корзины пользователя.
        """
        repo = CartRepository(db_session)
        try:
            items = await repo.get_cart_items_by_user_id(chat_id)
            return [
                {
                    "id": item.id,
                    "user_id": item.user_id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "total_price": item.total_price
                }
                for item in items
            ]
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
        - Словарь с результатом операции и статусом.
        """
        repo = CartRepository(db_session)
        try:
            updated_item = await repo.update_cart_item(chat_id, item_id, data)
            return {
                "message": "Элемент корзины успешно обновлён.",
                "data": updated_item
            }
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
        - Словарь с результатом операции и статусом.
        """
        repo = CartRepository(db_session)
        try:
            removed_item = await repo.remove_from_cart(chat_id, item_id)
            return {
                "message": "Элемент успешно удалён из корзины.",
                "data": removed_item
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
