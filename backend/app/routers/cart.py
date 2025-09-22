from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.cart import CartItemCreate, UpdateCartItemSchema
from schemas.view_cart_schema import ViewCartSchema
from services.cart_service import CartService
from dependencies import get_db

router = APIRouter(tags=["Корзина покупок"])


@router.post("/item-cart/", summary="Добавить товар в корзину",
             response_model=dict)
async def add_to_cart(cart_item: CartItemCreate,
                      db: AsyncSession = Depends(get_db)):
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
    async with db as session:
        return await CartService.add_to_cart(cart_item, session)


@router.get("/item-cart/{chat_id}",
            summary="Получить список товаров в корзине",
            response_model=ViewCartSchema)
async def view_cart(chat_id: int, db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Просмотр содержимого корзины пользователя.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.

    #### Ответ:
    Содержимое корзины пользователя с итоговой суммой.
    """
    async with db as session:
        return await CartService.view_cart(chat_id, session)


@router.put("/item-cart/{chat_id}/{item_id}",
            summary="Изменить количество товара в корзине")
async def update_cart_item(chat_id: int, item_id: int,
                           data: UpdateCartItemSchema,
                           db: AsyncSession = Depends(get_db)):
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
    async with db as session:
        return await CartService.update_cart_item(chat_id, item_id,
                                                  data, session)


@router.delete("/item-cart/{chat_id}/{item_id}",
               summary="Удалить товар из корзины")
async def remove_from_cart(chat_id: int, item_id: int,
                           db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Удаление товара из корзины пользователя.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.
    - `item_id`: Идентификатор товара в корзине.

    #### Ответ:
    Сообщение о том, что товар удалён из корзины.
    """
    async with db as session:
        return await CartService.remove_from_cart(chat_id, item_id, session)
