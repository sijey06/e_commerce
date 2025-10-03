from dependencies import get_db
from fastapi import APIRouter, Depends
from schemas.category import (CategoryCreate, CategoryResponse,
                              CategoryResponseList)
from services.category_service import CategoryService
from sqlalchemy.ext.asyncio import AsyncSession

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


@router.put("/categories/{category_id}/", summary="Изменение категории",
            response_model=CategoryResponse)
async def edit_category(category_id: int, new_name: str,
                        db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Изменение имени существующей категории.

    #### Входящие данные:
    - `category_id`: Идентификатор категории.
    - `new_name`: Новое название категории.

    #### Ответ:
    Отредактированная категория.
    """
    async with db as session:
        updated_category = await CategoryService.update_category(
            category_id, new_name, session)
        return updated_category


@router.delete("/categories/{category_id}/", summary="Удаление категории",
               response_model=dict)
async def remove_category(category_id: int,
                          db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Удаление категории по её идентификатору.

    #### Входящие данные:
    - `category_id`: Идентификатор категории.

    #### Ответ:
    Сообщение об успешном удалении категории.
    """
    async with db as session:
        removed_category = await CategoryService.delete_category(
            category_id, session)
        return removed_category
