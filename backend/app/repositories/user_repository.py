from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from schemas.user import UserCreate


class UserRepository:
    """Класс для работы с пользователями."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_create: UserCreate):
        """Создание нового пользователя."""
        db_user = User(**user_create.model_dump())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get_user_by_chat_id(self, chat_id: int):
        """Получение заказов пользователя по чат-ID."""
        stmt = select(User).where(User.chat_id == chat_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
