from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass


# Создание движка для базы данных
engine = create_async_engine(
    DATABASE_URL.replace('postgresql', 'postgresql+asyncpg'), echo=False)

# Глобальная фабрика сессий
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)
