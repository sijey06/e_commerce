from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.cart import CartItem
from models.product import Product
from schemas.cart import CartItemCreate, CartItemResponse, UpdateCartItemSchema
from schemas.user import UserCreate
from services.user_service import UserService


class CartRepository:
    """Класс для хранения операций с корзинами"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _fetch_user_and_register_if_needed(self, chat_id: int):
        """
        Получение пользователя по чат ID или регистрация нового пользователя.
        Возвращает объект пользователя.
        """
        user_service = UserService()
        user = await user_service.fetch_user_by_chat_id(chat_id, self.session)
        if not user:
            new_user = UserCreate(first_name='', address='',
                                  phone_number=0, chat_id=chat_id)
            registered_user = await user_service.register_user(
                new_user, self.session)
            user = registered_user['data']
        return user

    async def add_to_cart(self, cart_item_create: CartItemCreate):
        """Добавление товара в корзину пользователя"""
        try:
            user = await self._fetch_user_and_register_if_needed(
                cart_item_create.chat_id)
            product = await self.session.get(
                Product, cart_item_create.product_id)
            if not product:
                raise ValueError('Продукт не найден.')
            stmt = select(CartItem).filter_by(
                chat_id=user.chat_id, product_id=cart_item_create.product_id)
            result = await self.session.execute(stmt)
            existing_item = result.scalars().first()
            if existing_item:
                existing_item.quantity += cart_item_create.quantity
                existing_item.total_price = (
                    product.price * existing_item.quantity)
            else:
                total_price = product.price * cart_item_create.quantity
                new_item = CartItem(
                    chat_id=user.chat_id,
                    product_id=product.id,
                    quantity=cart_item_create.quantity,
                    total_price=total_price
                )
                self.session.add(new_item)
                existing_item = new_item
            await self.session.commit()
            await self.session.refresh(existing_item)
            return CartItemResponse.model_validate(existing_item).model_dump()
        except IntegrityError as e:
            print(f'Ошибка целостности данных: {e}')

    async def find_cart_item_by_product(self, chat_id: int, product_id: int):
        """Поиск элемента корзины по продукту"""
        stmt = select(CartItem).filter_by(chat_id=chat_id,
                                          product_id=product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_cart_item(self, chat_id: int,
                               product_id: int, data: UpdateCartItemSchema):
        """Обновление элемента корзины"""
        product = await self.session.get(Product, product_id)
        if not product:
            raise Exception('Продукт не найден.')
        cart_item = await self.find_cart_item_by_product(chat_id, product_id)
        if not cart_item:
            raise Exception('Товар не найден в корзине.')
        updated_data = data.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(cart_item, key, value)
        if 'quantity' in updated_data:
            cart_item.total_price = product.price * cart_item.quantity
        await self.session.commit()
        await self.session.refresh(cart_item)
        return cart_item

    async def get_cart_items_by_user_id(self, chat_id: int) -> List[CartItem]:
        """Получение элементов корзины по идентификатору пользователя"""
        stmt = select(
            CartItem).options(selectinload(
                CartItem.product).selectinload(
                    Product.category)).filter_by(chat_id=chat_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def clear_cart(self, chat_id: int):
        """Очистка корзины пользователя"""
        stmt = select(CartItem).filter_by(chat_id=chat_id)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        for item in items:
            await self.session.delete(item)
        await self.session.commit()

    async def remove_from_cart(self, chat_id: int, product_id: int):
        """Удаление конкретного элемента из корзины"""
        cart_item = await self.find_cart_item_by_product(chat_id, product_id)
        if not cart_item:
            raise Exception('Товар не найден в корзине.')
        await self.session.delete(cart_item)
        await self.session.commit()
