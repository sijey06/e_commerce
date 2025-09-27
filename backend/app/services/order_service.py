from fastapi import HTTPException

from services.user_service import UserService
from repositories.order_repository import OrderRepository
from repositories.cart_repository import CartRepository
from models.product import Product
from schemas.order import OrderCreate, OrderResponse
from schemas.user import UserCreate
from schemas.status import OrderStatusUpdate


class OrderService:
    """Класс для управления заказами."""

    @staticmethod
    async def create_order(order_data: OrderCreate, db_session):
        """
        Создание нового заказа.

        Параметры:
        - order_create (OrderCreate): Данные для создания нового заказа.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Словарь с информацией о новом заказе и сообщение
        об успешной операции.
        """
        user_service = UserService()
        user = await user_service.fetch_user_by_chat_id(order_data.chat_id,
                                                        db_session)
        if user is None:
            raise Exception("Пользователь не найден.")
        cart_repo = CartRepository(db_session)
        cart_items = await cart_repo.get_cart_items_by_user_id(
            order_data.chat_id)
        if not cart_items:
            raise Exception("Корзина пуста, невозможно оформить заказ.")
        order_details = {
            "user_id": user.id,
            "status": order_data.status
        }
        repository = OrderRepository(db_session)
        created_order = await repository.create_order(order_details)
        products_in_order = [await db_session.get(
            Product, item.product_id) for item in cart_items]
        created_order.ordered_products.extend(products_in_order)
        await db_session.commit()
        await db_session.refresh(created_order)
        await cart_repo.clear_cart(order_data.chat_id)
        return OrderResponse.model_validate(created_order)

    @staticmethod
    async def retrieve_order_by_id(order_id: int, db_session):
        """
        Получение заказа по его ID.

        Параметры:
        - order_id (int): Уникальный идентификатор заказа.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Заказ, найденный по указанному ID, или исключение 404,
        если заказ не найден.
        """
        repo = OrderRepository(db_session)
        try:
            found_order = await repo.get_order_by_id(order_id)
            if found_order is None:
                raise HTTPException(status_code=404, detail="Заказ не найден.")
            return found_order
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def retrieve_all_orders(db_session):
        """
        Получение списка всех заказов.

        Параметры:
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Список всех доступных заказов.
        """
        repo = OrderRepository(db_session)
        try:
            all_orders = await repo.get_all_orders()
            return all_orders
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def update_order_status(order_id: int,
                                  status_data: OrderStatusUpdate, db_session):
        """
        Обновление статуса заказа.

        Параметры:
        - order_id (int): Уникальный идентификатор заказа.
        - status_data (OrderStatusUpdate): Данные для обновления
        статуса заказа.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Обновлённый заказ с новым статусом.
        """
        repo = OrderRepository(db_session)
        try:
            updated_order = await repo.update_order_status(order_id,
                                                           status_data.status)
            return updated_order
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def list_orders_by_user_id(user_id: int, db_session):
        """
        Получение списка заказов конкретного пользователя.

        Параметры:
        - user_id (int): Уникальный идентификатор пользователя.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Список заказов, принадлежащих данному пользователю.
        """
        repo = OrderRepository(db_session)
        try:
            user_orders = await repo.list_orders_by_user_id(user_id)
            orders_list = [
                OrderResponse.model_validate(order) for order in user_orders]
            return orders_list
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
