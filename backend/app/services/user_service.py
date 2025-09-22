from fastapi import HTTPException
from repositories.user_repository import UserRepository
from schemas.user import UserCreate


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
        try:
            registered_user = await repo.create_user(user_create)
            return {
                "message": "Пользователь зарегистрирован успешно.",
                "data": registered_user
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

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
        try:
            found_user = await repo.get_user_by_chat_id(chat_id)
            if found_user is None:
                raise HTTPException(status_code=404,
                                    detail="Пользователь не найден.")
            return found_user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
