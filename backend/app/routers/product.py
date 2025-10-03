from dependencies import get_db
from fastapi import APIRouter, Depends
from schemas.product import ProductCreate, ProductResponse, ProductUpdate
from services.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Товары"])


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


@router.get("/products/",
            summary="Получение списка всех товаров",
            response_model=list[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Получение списка всех товаров, имеющихся в магазине.

    #### Ответ:
    Полный список товаров магазина.
    """
    async with db as session:
        return await ProductService.retrieve_all_products(session)


@router.get("/products/{product_id}", summary="Получение товара по ID",
            response_model=ProductResponse)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Получение подробной информации о конкретном товаре
    по его уникальному идентификатору.

    #### Входящие данные:
    - `product_id`: Уникальный идентификатор товара.

    #### Ответ:
    Полная информация о данном товаре.
    """
    async with db as session:
        return await ProductService.retrieve_product_by_id(product_id, session)


@router.put("/products/{product_id}/", summary="Редактирование товара",
            response_model=ProductResponse)
async def edit_product(product_id: int, updates: ProductUpdate,
                       db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Редактирование существующих данных товара.

    #### Входящие данные:
    - `product_id`: Идентификатор товара.
    - `updates`: Изменённые поля товара (например, название, цена, описание).

    #### Ответ:
    Отредактированный объект товара.
    """
    async with db as session:
        updated_product = await ProductService.update_product(
            product_id, updates.model_dump(), session)
        return updated_product


@router.delete("/products/{product_id}/", summary="Удаление товара",
               response_model=dict)
async def remove_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Удаление товара по его идентификатору.

    #### Входящие данные:
    - `product_id`: Идентификатор товара.

    #### Ответ:
    Сообщение об успешном удалении товара.
    """
    async with db as session:
        removed_product = await ProductService.delete_product(
            product_id, session)
        return removed_product
