from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.category import Category
from schemas.category import CategoryCreate


class CategoryRepository:
    """Класс для работы с категориями."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, category_create: CategoryCreate):
        """Создание новой категории."""
        db_category = Category(name=category_create.name)
        self.session.add(db_category)
        await self.session.commit()
        await self.session.refresh(db_category)
        return db_category

    async def get_category_by_id(self, category_id: int):
        """Получить категорию по её ID."""
        stmt = select(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all_categories(self):
        """Получить все доступные категории."""
        stmt = select(Category)
        result = await self.session.execute(stmt)
        return result.scalars().all()
