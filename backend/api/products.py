from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.models import (Category, CartItem, Product, User,
                           product_category_association)
from schemas.schemas import (ProductResponse, CategoryCreate, AddToCartSchema,
                             UpdateCartItemSchema, ViewCartSchema,
                             ViewCartItemSchema)
from core.utils import (calculate_and_update_cart_item, get_cart_item,
                        get_category, get_product, get_user)
from core.database import get_db


app = APIRouter()


@app.get("/products/",
         summary="Получение списка всех товаров",
         tags=["Продукты"],
         response_model=List[ProductResponse])
async def list_products(db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Получение списка всех товаров, имеющихся в магазине.

    #### Ответ:
    Полный список товаров магазина.
    """
    products = db.query(Product).all()
    return products


@app.get("/products/{product_id}",
         summary="Получение товара по ID",
         tags=["Продукты"],
         response_model=ProductResponse)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Получение подробной информации о конкретном товаре
    по его уникальному идентификатору.

    #### Входящие данные:
    - `product_id`: Уникальный идентификатор товара.

    #### Ответ:
    Полная информация о данном товаре.
    """
    product = get_product(product_id, db)
    return product


@app.post("/categories/", summary="Создание новой категории",
          tags=["Продукты"])
async def create_category(category_data: CategoryCreate,
                          db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Создание новой категории товаров.

    #### Входящие данные:
    - `name`: Название категории.

    #### Ответ:
    Информация о вновь созданной категории.
    """
    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@app.get("/categories/", summary="Получение списка всех категорий",
         tags=["Продукты"])
async def list_categories(db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Получение списка всех категорий товаров.

    #### Ответ:
    Полный список категорий товаров.
    """
    categories = db.query(Category).all()
    return categories


@app.get("/categories/{category_id}",
         summary="Получить товары выбранной категории", tags=["Продукты"])
async def get_products_by_category(category_id: int,
                                   db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Получение списка товаров определенной категории.

    #### Входящие данные:
    - `category_id`: Уникальный идентификатор категории.

    #### Ответ:
    Список товаров, принадлежащих указанной категории.
    """
    get_category(category_id, db)
    products = db.query(Product).join(
        product_category_association).filter(
            product_category_association.c.category_id == category_id).all()

    return products


@app.post("/item-cart/", summary="Добавить товар в корзину",
          tags=["Корзина покупок"])
async def add_to_cart(cart_item: AddToCartSchema,
                      db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Добавление товара в корзину пользователя.

    #### Входящие данные:
    - `product_id`: Идентификатор товара.
    - `quantity`: Количество единиц товара (по умолчанию 1).
    - `chat_id`: Уникальный идентификатор чата пользователя.

    #### Ответ:
    Сообщение о успешном добавлении товара в корзину.
    """
    user = db.query(User).filter(User.chat_id == cart_item.chat_id).first()
    if not user:
        user = User(chat_id=cart_item.chat_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    product = get_product(cart_item.product_id, db)

    existing_item = db.query(CartItem).filter(
        CartItem.product_id == cart_item.product_id).first()

    if existing_item:
        calculate_and_update_cart_item(existing_item,
                                       product, cart_item.quantity)
    else:
        new_item = CartItem(
            user_id=user.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            total_price=product.price * cart_item.quantity
        )
        db.add(new_item)

    db.commit()
    return {"message": "Товар добавлен в корзину"}


@app.get("/item-cart/{chat_id}", summary="Просмотреть корзину пользователя",
         tags=["Корзина покупок"], response_model=ViewCartSchema)
async def view_cart(chat_id: int, db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Отображение содержимого корзины пользователя.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.

    #### Ответ:
    Содержимое корзины пользователя с итоговой суммой.
    """
    user = get_user(chat_id, db)
    items_raw = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    items = [
        ViewCartItemSchema.model_validate(c) for c in items_raw
    ]
    grand_total = sum(item.total_price for item in items)
    return ViewCartSchema(cart_items=items, grand_total=grand_total)


@app.put("/item-cart/{chat_id}/{item_id}", tags=["Корзина покупок"],
         summary="Изменить количество товара в корзине")
async def update_cart_item(chat_id: int, item_id: int,
                           data: UpdateCartItemSchema,
                           db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Изменение количества выбранного товара в корзине пользователя.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.
    - `item_id`: Идентификатор товара в корзине.
    - `data`: Данные для обновления (количество товара).

    #### Ответ:
    Сообщение о том, что количество товара обновлено.
    """
    user = get_user(chat_id, db)
    item = get_cart_item(item_id, user.id, db)
    product = get_product(item.product_id, db)
    item.quantity = data.quantity
    item.total_price = product.price * data.quantity
    db.commit()
    return {"message": "Количество товара обновлено"}


@app.delete("/item-cart/{chat_id}/{item_id}", tags=["Корзина покупок"],
            summary="Удалить товар из корзины")
async def remove_from_cart(chat_id: int, item_id: int,
                           db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Удаление товара из корзины пользователя.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.
    - `item_id`: Идентификатор товара в корзине.

    #### Ответ:
    Сообщение о том, что товар удалён из корзины.
    """
    user = get_user(chat_id, db)
    item = get_cart_item(item_id, user.id, db)
    db.delete(item)
    db.commit()
    return {"message": "Товар удален из корзины"}
