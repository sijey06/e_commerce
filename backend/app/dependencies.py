from contextlib import asynccontextmanager

from database import SessionLocal


@asynccontextmanager
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
