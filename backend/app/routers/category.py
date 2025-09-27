from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.category import (CategoryCreate, CategoryResponse,
                              CategoryResponseList)
from services.category_service import CategoryService
from dependencies import get_db

router = APIRouter(tags=["Категории"])


@router.post("/categories/", summary="Создание новой категории",
             response_model=CategoryResponse)
async def create_category(category: CategoryCreate,
                          db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Создание новой категории товаров.

    #### Входящие данные:
    - `name`: Название категории.

    #### Ответ:
    Информация о вновь созданной категории.
    """
    async with db as session:
        return await CategoryService.create_category(category, session)


@router.get("/categories/", summary="Получение списка всех категорий",
            response_model=list[CategoryResponseList])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Получение списка всех категорий товаров.

    #### Ответ:
    Полный список категорий товаров.
    """
    async with db as session:
        return await CategoryService.list_categories(session)


@router.get("/categories/{category_id}",
            summary="Получить товары выбранной категории",
            response_model=CategoryResponse)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Получение списка товаров определенной категории.

    #### Входящие данные:
    - `category_id`: Уникальный идентификатор категории.

    #### Ответ:
    Список товаров, принадлежащих указанной категории.
    """
    async with db as session:
        return await CategoryService.find_category_by_id(category_id, session)
