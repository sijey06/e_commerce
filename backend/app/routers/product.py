from dependencies import get_db
from fastapi import APIRouter, Depends
from schemas.product import ProductResponse
from services.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Продукты"])


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
