from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from models.models import CartItem, User, Order
from schemas.schemas import CreateOrderSchema, OrderResponse
from core.database import get_db
from core.utils import get_user


app = APIRouter()


@app.post("/orders/", summary="Создать новый заказ",
          tags=["Пользователи"])
async def create_order(order_data: CreateOrderSchema,
                       db: Session = Depends(get_db)):
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
    user = db.query(User).filter(User.chat_id == order_data.chat_id).first()
    if not user:
        user = User(first_name=order_data.first_name,
                    address=order_data.address,
                    phone_number=int(order_data.phone_number),
                    chat_id=order_data.chat_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    cart = db.query(CartItem).filter(
        CartItem.user_id == user.id).all()
    if not cart:
        raise HTTPException(status_code=404, detail="Корзина не найдена")
    new_order = Order(user=user)
    db.add(new_order)
    db.flush()
    for item in cart:
        new_order.ordered_products.append(item.product)
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    db.refresh(new_order)
    return {"order_id": new_order.id, "status": new_order.status}


@app.get("/orders/{chat_id}", tags=["Пользователи"],
         response_model=List[OrderResponse],
         summary="Получить список заказов пользователя")
async def list_orders(chat_id: int, db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Получение списка заказов определенного пользователя.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.

    #### Ответ:
    Список объектов заказов пользователя, с информацией о каждом заказе.
    """
    user = get_user(chat_id, db)
    orders = db.query(Order).options(joinedload(Order.products)).filter(
        Order.user_id == user.id).all()
    return orders
