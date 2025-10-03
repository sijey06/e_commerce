from fastapi import HTTPException
from repositories.category_repository import CategoryRepository
from schemas.category import CategoryCreate, CategoryResponse


class CategoryService:
    """Класс для управления категориями."""

    @staticmethod
    async def create_category(category_create: CategoryCreate, db_session):
        """
        Создание новой категории.

        Параметры:
        - category_create (CategoryCreate): Данные для создания
        новой категории.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Словарь с информацией о созданной категории и статусным сообщением.
        """
        repo = CategoryRepository(db_session)
        try:
            created_category = await repo.create_category(category_create)
            serialized_product = CategoryResponse.model_validate(
                created_category)
            return serialized_product
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def find_category_by_id(category_id: int, db_session):
        """
        Получение категории по её ID.

        Параметры:
        - category_id (int): Уникальный идентификатор категории.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Экземпляр категории, найденной по указанному ID,
        или исключение 404, если категория не найдена.
        """
        repo = CategoryRepository(db_session)
        try:
            found_category = await repo.get_category_by_id(category_id)
            if found_category is None:
                raise HTTPException(status_code=404,
                                    detail="Категория не найдена.")
            return found_category
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def list_categories(db_session):
        """
        Получение списка всех существующих категорий.

        Параметры:
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Список всех доступных категорий.
        """
        repo = CategoryRepository(db_session)
        try:
            categories_list = await repo.find_all_categories()
            return categories_list
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def update_category(category_id: int, new_name: str, db_session):
        """
        Обновляет название категории.

        Параметры:
        - category_id (int): Идентификатор категории.
        - new_name (str): Новое название категории.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Объект обновленной категории или ошибку 404,
        если категория не найдена.
        """
        repo = CategoryRepository(db_session)
        try:
            updated_category = await repo.update_category(
                category_id, new_name)
            if updated_category is None:
                raise HTTPException(status_code=404,
                                    detail="Категория не найдена")
            return updated_category
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_category(category_id: int, db_session):
        """
        Удаляет категорию по её идентификатору.

        Параметры:
        - category_id (int): Идентификатор удаляемой категории.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Результат успешного удаления (True) или ошибку 404,
        если категория не найдена.
        """
        repo = CategoryRepository(db_session)
        try:
            deleted_result = await repo.delete_category(category_id)
            if not deleted_result:
                raise HTTPException(status_code=404,
                                    detail="Категория не найдена")
            return {"message": f"Категория с id={category_id} успешно удалена"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
