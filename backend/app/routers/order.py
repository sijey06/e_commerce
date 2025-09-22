from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.product import ProductCreate, ProductResponse
from schemas.order import OrderResponse
from schemas.status import OrderStatusUpdate
from services.order_service import OrderService
from services.product_service import ProductService
from dependencies import get_db

router = APIRouter(tags=["Админ-панель"])


@router.post("/products/", summary="Создание нового товара",
             response_model=ProductResponse)
async def create_product(product: ProductCreate, category_id: int,
                         db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Создание нового товара.

    #### Входящие данные:
    - `name`: Название товара.
    - `description`: Описание товара.
    - `price`: Цена товара.
    - `photo_url`: Опциональный адрес фотографии товара.

    #### Ответ:
    Информация о вновь созданном товаре.
    """
    async with db as session:
        return await ProductService.create_new_product(product,
                                                       category_id, session)


@router.get("/orders/", summary="Получение списка всех заказов",
            response_model=list[OrderResponse])
async def list_all_orders(db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Получение полного списка всех заказов в системе.

    #### Ответ:
    Список всех заказов, включающих подробную информацию
    о продуктах каждого заказа.
    """
    async with db as session:
        return await OrderService.retrieve_all_orders(session)


@router.put("/orders-status/{order_id}", summary="Обновление статуса заказа",
            response_model=OrderResponse)
async def update_order_status(order_id: int, status_data: OrderStatusUpdate,
                              db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Обновить статус заказа.

    #### Входящие данные:
    - `order_id`: Уникальный идентификатор заказа.
    - `status`: Статус заказа.

    #### Доступные статусы:
    - `NEW` = **НОВЫЙ**
    - `IN_PROGRESS` = **В ОБРАБОТКЕ**
    - `SENT` = **ОТПРАВЛЕН**

    #### Ответ:
    Возвращает словарь с двумя ключевыми полями:
    - **status**: Новый статус заказа.
    - **id**: Идентификатор заказа.
    """
    async with db as session:
        return await OrderService.update_order_status(order_id,
                                                      status_data, session)
