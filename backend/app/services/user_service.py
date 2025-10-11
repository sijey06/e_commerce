from fastapi import HTTPException

from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserEdit


class UserService:
    """Класс для управления пользователями."""

    @staticmethod
    async def register_user(user_create: UserCreate, db_session):
        """
        Регистрация нового пользователя.

        Параметры:
        - user_create (UserCreate): Данные для регистрации нового пользователя.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Словарь с информацией о зарегистрированном пользователе
        и успешным сообщением.
        """
        repo = UserRepository(db_session)
        existing_user = await repo.get_user_by_chat_id(user_create.chat_id)
        if existing_user:
            raise HTTPException(status_code=409,
                                detail="Пользователь уже зарегистрирован.")
        registered_user = await repo.create_user(user_create)
        return registered_user

    @staticmethod
    async def fetch_user_by_chat_id(chat_id: int, db_session):
        """
        Получение пользователя по его Chat ID.

        Параметры:
        - chat_id (int): Чат-идентификатор пользователя.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Пользователь, найденный по указанному Chat ID,
        или исключение 404, если пользователь не найден.
        """
        repo = UserRepository(db_session)
        found_user = await repo.get_user_by_chat_id(chat_id)
        if not found_user:
            raise HTTPException(status_code=404,
                                detail="Пользователь не найден.")
        return found_user

    @staticmethod
    async def update_user(updates: UserEdit, chat_id: int, db_session):
        """
        Обновление данных пользователя.
        """
        repo = UserRepository(db_session)
        user = await repo.get_user_by_chat_id(chat_id)
        if not user:
            raise HTTPException(status_code=404,
                                detail="Пользователь не найден.")
        if updates.first_name:
            user.first_name = updates.first_name
        if updates.address:
            user.address = updates.address
        if updates.phone_number:
            user.phone_number = updates.phone_number
        await db_session.commit()
        await db_session.refresh(user)
        return user

    @staticmethod
    async def fetch_all_users(db_session):
        """
        Получение всех пользователей из базы данных.

        Параметры:
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Список всех зарегистрированных пользователей.
        """
        repo = UserRepository(db_session)
        return await repo.get_all_users()
