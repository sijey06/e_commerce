from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas.user import UserCreate, UserResponse, UserEdit
from services.user_service import UserService

router = APIRouter(tags=["Пользователи"])


@router.post("/register/", summary="Регистрация нового пользователя",
             response_model=UserResponse)
async def register_user(user_create: UserCreate = Body(...),
                        db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Регистрация нового пользователя.

    #### Входящие данные:
    - `first_name`: Имя пользователя.
    - `address`: Адрес пользователя.
    - `phone_number`: Номер телефона пользователя.
    - `chat_id`: Учетный идентификатор чата пользователя.

    #### Ответ:
    Информация о зарегистрированном пользователе.
    """
    async with db as session:
        return await UserService.register_user(user_create, session)


@router.get("/user/{chat_id}/", summary="Получение пользователя по Chat ID",
            response_model=UserResponse)
async def get_user_by_chat_id(
    chat_id: int = Path(..., description="Chat ID пользователя"),
    db: AsyncSession = Depends(get_db)
):
    """
    ### Цель метода:
    Получение информации о пользователе по его Chat ID.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.

    #### Ответ:
    Подробная информация о запрашиваемом пользователе.
    """
    async with db as session:
        return await UserService.fetch_user_by_chat_id(chat_id, session)


@router.patch("/user/{chat_id}/", summary="Изменение данных пользователя",
              response_model=UserResponse)
async def update_user_data(
    chat_id: int = Path(..., description="Chat ID пользователя"),
    updates: UserEdit = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    ### Цель метода:
    Изменение персональных данных пользователя.

    #### Входящие данные:
    - `chat_id`: Уникальный идентификатор чата пользователя.
    - `updates`: Поля для изменения (например, имя, адрес, телефон).

    #### Ответ:
    Обновленные данные пользователя.
    """
    async with db as session:
        return await UserService.update_user(updates, chat_id, session)


@router.get("/users/", summary="Получение всех пользователей",
            response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """
    ### Цель метода:
    Получение полного списка всех зарегистрированных пользователей.

    #### Ответ:
    Массив объектов с информацией обо всех пользователях.
    """
    async with db as session:
        return await UserService.fetch_all_users(session)
