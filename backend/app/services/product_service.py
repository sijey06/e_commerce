from fastapi import HTTPException
from repositories.product_repository import ProductRepository
from schemas.product import ProductCreate, ProductResponse
from sqlalchemy import select
from models.category import Category


class ProductService:
    """Класс для управления товарами."""

    @staticmethod
    async def create_new_product(product_create: ProductCreate,
                                 category_id: int, db_session):
        """
        Создание нового товара.

        Параметры:
        - product_create (ProductCreate): Данные для создания нового товара.
        - category_id (int): ID категории, к которой относится товар.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Словарь с информацией о созданном товаре и
        сообщение об успешной операции.
        """
        repo = ProductRepository(db_session)
        try:
            created_product = await repo.create_product(
                product_create, category_id)
            category_stmt = select(Category).where(Category.id == category_id)
            category = await db_session.execute(category_stmt)
            category_obj = category.scalar_one_or_none()
            product_dict = {
                "id": created_product.id,
                "name": created_product.name,
                "description": created_product.description,
                "price": created_product.price,
                "photo_url": created_product.photo_url,
                "categories": category_obj
            }
            serialized_product = ProductResponse.model_validate(product_dict)
            return serialized_product
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def retrieve_product_by_id(product_id: int, db_session):
        """
        Получение товара по его ID.

        Параметры:
        - product_id (int): Уникальный идентификатор товара.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Объект товара, найденный по указанному ID, или исключение 404,
        если товар не найден.
        """
        repo = ProductRepository(db_session)
        try:
            found_product = await repo.get_product_by_id(product_id)
            if found_product is None:
                raise HTTPException(status_code=404, detail="Товар не найден.")
            return found_product
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def retrieve_all_products(db_session):
        """
        Получение списка всех товаров.

        Параметры:
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Список всех имеющихся товаров.
        """
        repo = ProductRepository(db_session)
        try:
            products_list = await repo.get_all_products()
            return products_list
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def update_product(product_id: int, updated_data: dict, db_session):
        """
        Обновляет информацию о существующем товаре.

        Параметры:
        - product_id (int): Идентификатор товара.
        - updated_data (dict): Данные для обновления товара.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Объект обновленного товара или ошибку 404, если товар не найден.
        """
        repo = ProductRepository(db_session)
        try:
            updated_product = await repo.update_product(
                product_id, updated_data)
            if updated_product is None:
                raise HTTPException(status_code=404, detail="Товар не найден")
            return updated_product
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_product(product_id: int, db_session):
        """
        Удаляет товар по его идентификатору.

        Параметры:
        - product_id (int): Идентификатор удаляемого товара.
        - db_session: Текущая сессия базы данных.

        Возвращает:
        - Результат успешного удаления (True) или ошибка 404,
        если товар не найден.
        """
        repo = ProductRepository(db_session)
        try:
            deleted_result = await repo.delete_product(product_id)
            if not deleted_result:
                raise HTTPException(status_code=404, detail="Товар не найден")
            return {"message": f"Товар с id={product_id} успешно удалён."}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
