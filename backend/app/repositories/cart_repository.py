from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.cart import CartItem
from schemas.cart import CartItemCreate, UpdateCartItemSchema


class CartRepository:
    """Класс для хранения операций с корзинами"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_cart(self, cart_item_create: CartItemCreate):
        """Добавляет товар в корзину"""
        cart_item = CartItem(**cart_item_create.model_dump())
        self.session.add(cart_item)
        await self.session.commit()
        await self.session.refresh(cart_item)
        return cart_item

    async def get_cart_items_by_user_id(self, chat_id: int) -> List[CartItem]:
        """Получает элементы корзины по идентификатору пользователя"""
        stmt = select(CartItem).where(CartItem.user_id == chat_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_cart_item(self, chat_id: int, item_id: int,
                               data: UpdateCartItemSchema):
        """Обновляет элемент корзины"""
        stmt = select(CartItem).where(
            (CartItem.user_id == chat_id) & (CartItem.id == item_id))
        result = await self.session.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if cart_item is None:
            raise Exception("Товар не найден в корзине.")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(cart_item, key, value)

        await self.session.commit()
        await self.session.refresh(cart_item)
        return cart_item

    async def remove_from_cart(self, chat_id: int, item_id: int):
        """Удаляет элемент из корзины"""
        stmt = select(CartItem).where(
            (CartItem.user_id == chat_id) & (CartItem.id == item_id))
        result = await self.session.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if cart_item is None:
            raise Exception("Товар не найден в корзине.")

        await self.session.delete(cart_item)
        await self.session.commit()
        return True
