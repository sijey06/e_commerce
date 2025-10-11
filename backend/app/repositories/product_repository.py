from models.category import Category
from models.product import Product
from schemas.product import ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload


class ProductRepository:
    """Класс для работы с товарами."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product_create: ProductCreate,
                             category_id: int):
        """Создание нового товара."""
        category = await self.session.get(Category, category_id)
        if category is None:
            raise Exception("Категория не найдена.")
        db_product = Product(**product_create.model_dump())
        db_product.category.append(category)
        self.session.add(db_product)
        await self.session.commit()
        await self.session.refresh(db_product)
        return db_product

    async def get_product_by_id(self, product_id: int):
        """Получение товара по его ID."""
        stmt = select(
            Product).options(
                selectinload(
                    Product.category)).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_products(self):
        """Получение всех товаров."""
        stmt = select(Product).options(joinedload(Product.category))
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def update_product(self, product_id: int, updated_data: dict):
        """Обновляет существующий продукт"""
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        product_to_update = result.scalar_one_or_none()

        for key, value in updated_data.items():
            setattr(product_to_update, key, value)

        await self.session.commit()
        await self.session.refresh(product_to_update)
        return product_to_update

    async def delete_product(self, product_id: int):
        """Удаляет продукт по его идентификатору"""
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        product_to_delete = result.scalar_one_or_none()
        await self.session.delete(product_to_delete)
        await self.session.commit()
        return True
