from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from schemas.order import OrderResponse
from schemas.user import UserResponse
from services.order_service import OrderService, OrderCreate
from services.user_service import UserService
from dependencies import get_db

router = APIRouter(tags=["Пользователи"])


@router.post("/orders/", summary="Создать новый заказ",
             response_model=OrderResponse)
async def create_order(order: OrderCreate,
                       db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Создание нового заказа пользователя.

    #### Входящие данные:
    - `first_name`: Имя заказчика.
    - `address`: Адрес доставки.
    - `phone_number`: Телефон заказчика.
    - `chat_id`: Уникальный идентификатор чата пользователя.

    #### Ответ:
    Возвращает словарь с двумя ключевыми полями:
    - **order_id**: Идентификатор созданного заказа.
    - **status**: Текущий статус заказа (по умолчанию `НОВЫЙ`).
    """
    try:
        async with db as session:  # Здесь стартует транзакция
            service = OrderService()
            created_order = await service.create_order(order, session)
            return created_order
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/orders/{chat_id}",
            summary="Получить список заказов пользователя",
            response_model=list[UserResponse])
async def list_orders(chat_id: int, db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Получение списка заказов определенного пользователя.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.

    #### Ответ:
    Список объектов заказов пользователя, с информацией о каждом заказе.
    """
    async with db as session:
        user = await UserService.fetch_user_by_chat_id(chat_id, session)
        orders = await OrderService.list_orders_by_user_id(user.id, session)
        return orders
