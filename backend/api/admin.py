from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from models.models import Product, Order
from schemas.schemas import (ProductCreate, ProductResponse, OrderStatusCreate,
                             OrderStatusResponse, OrderResponse)

from core.database import get_db
from core.status import Status
from core.utils import get_category


app = APIRouter()


@app.post("/products/",
          summary="Создание нового товара",
          tags=["Админ-панель"],
          response_model=ProductResponse)
async def create_product(product: ProductCreate, category_id: int,
                         db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Создание нового товара.

    #### Входящие данные:
    - `name`: Название товара.
    - `description`: Описание товара.
    - `price`: Цена товара.
    - `photo_url`: Опциональный адрес фотографии товара.
    - `category_id`: Идентификатор категории, к которой относится товар.

    #### Ответ:
    Информация о вновь созданном товаре.
    """
    category = get_category(category_id, db)
    new_product = Product(**product.model_dump())
    new_product.categories.append(category)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/orders/", response_model=List[OrderResponse], tags=["Админ-панель"],
         summary="Получить список всех заказов")
async def list_all_orders(db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Получение полного списка всех заказов в системе.

    #### Ответ:
    Список всех заказов, включающих подробную информацию
    о продуктах каждого заказа.
    """
    orders = db.query(Order).options(joinedload(Order.ordered_products)).all()
    result = []
    for order in orders:
        result.append(OrderResponse(
            id=order.id,
            status=order.status.value,
            products=[
                ProductResponse.from_orm(product)
                for product in order.ordered_products
                ]
                ))
    return result


@app.put("/orders-status/{order_id}",
         tags=["Админ-панель"],
         summary="Обновление статуса заказа",
         response_model=OrderStatusResponse)
async def update_order_status(order_id: int,
                              status_data: OrderStatusCreate,
                              db: Session = Depends(get_db)):
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
    existing_order = db.query(Order).filter(Order.id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    try:
        new_status = Status[status_data.status.upper()]
    except KeyError:
        raise HTTPException(status_code=400,
                            detail=f"Неверный статус '{status_data.status}'")
    existing_order.status = new_status
    db.commit()
    db.refresh(existing_order)
    return existing_order
