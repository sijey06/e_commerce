from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.order import Order
from schemas.order import OrderCreate
from schemas.status import Status


class OrderRepository:
    """Класс для работы с заказами."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order_create: OrderCreate):
        """Создание нового заказа."""
        db_order = Order(**order_create.model_dump())
        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)
        return db_order

    async def get_order_by_id(self, order_id: int):
        """Получение заказа по его ID."""
        stmt = select(Order).where(Order.id == order_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_orders(self):
        """Получение всех заказов."""
        stmt = select(Order)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_order_status(self, order_id: int, new_status: Status):
        """Обновление статуса заказа."""
        stmt = select(Order).where(Order.id == order_id)
        result = await self.session.execute(stmt)
        order = result.scalar_one_or_none()
        if not order:
            raise Exception(f"Заказ с ID {order_id} не найден")
        order.status = new_status
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def list_orders_by_user_id(self, user_id: int):
        """Получение списка заказов конкретного пользователя."""
        stmt = select(Order).where(Order.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
