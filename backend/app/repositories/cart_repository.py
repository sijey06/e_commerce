from typing import List

from models.cart import CartItem
from models.product import Product
from schemas.cart import CartItemCreate, CartItemResponse, UpdateCartItemSchema
from schemas.user import UserCreate
from services.user_service import UserService
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CartRepository:
    """Класс для хранения операций с корзинами"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_cart(self, cart_item_create: CartItemCreate):
        """Добавляет товар в корзину"""
        try:
            user_service = UserService()
            user = await user_service.fetch_user_by_chat_id(
                cart_item_create.chat_id, self.session)
            if user is None:
                user_create = UserCreate(first_name="", address="",
                                         phone_number=0,
                                         chat_id=cart_item_create.chat_id)
                registration_result = await user_service.register_user(
                    user_create, self.session)
                user = registration_result["data"]
            else:
                pass
            product = await self.session.get(Product,
                                             cart_item_create.product_id)
            if product is None:
                raise ValueError("Продукт не найден.")
            stmt = select(CartItem).where(
                CartItem.chat_id == user.chat_id,
                CartItem.product_id == cart_item_create.product_id
            )
            result = await self.session.execute(stmt)
            existing_item = result.scalars().first()
            if existing_item:
                existing_item.quantity += cart_item_create.quantity
                existing_item.total_price = (
                    product.price * existing_item.quantity)
                await self.session.commit()
                await self.session.refresh(existing_item)
                return CartItemResponse.model_validate(existing_item)
            else:
                total_price = product.price * cart_item_create.quantity
                cart_item = CartItem(
                    chat_id=user.chat_id,
                    product_id=product.id,
                    quantity=cart_item_create.quantity,
                    total_price=total_price
                )
                self.session.add(cart_item)
                await self.session.commit()
                await self.session.refresh(cart_item)
                return CartItemResponse.model_validate(cart_item).model_dump()
        except IntegrityError as e:
            print(f"Произошла ошибка целостности данных: {e}")

    async def find_cart_item_by_product(self, chat_id: int, product_id: int):
        """Находит элемент корзины по идентификатору продукта."""
        stmt = select(CartItem).where(
            (CartItem.chat_id == chat_id) &
            (CartItem.product_id == product_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_cart_item(self, chat_id: int, product_id: int,
                               data: UpdateCartItemSchema):
        """Обновляет элемент корзины."""
        product = await self.session.get(Product, product_id)
        if product is None:
            raise Exception("Продукт не найден.")
        cart_item = await self.find_cart_item_by_product(chat_id, product_id)
        if cart_item is None:
            raise Exception("Товар не найден в корзине.")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(cart_item, field, value)
        if 'quantity' in data.model_dump(exclude_unset=True):
            cart_item.total_price = product.price * cart_item.quantity
        await self.session.commit()
        await self.session.refresh(cart_item)
        return cart_item

    async def get_cart_items_by_user_id(self, chat_id: int) -> List[CartItem]:
        """Получает элементы корзины по идентификатору пользователя"""
        stmt = select(CartItem).where(CartItem.chat_id == chat_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def clear_cart(self, chat_id: int):
        """Очищает корзину пользователя"""
        stmt = select(CartItem).where(CartItem.chat_id == chat_id)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        for item in items:
            await self.session.delete(item)
        await self.session.commit()

    async def remove_from_cart(self, chat_id: int, product_id: int):
        """Удаляет конкретный элемент из корзины"""
        stmt = await self.find_cart_item_by_product(chat_id, product_id)
        if stmt is None:
            raise Exception("Товар не найден в корзине.")
        await self.session.delete(stmt)
        await self.session.commit()
        return True
