from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_CHATS


# Основная клавиатура
def create_main_keyboard(user_chat_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📌Каталог товаров", callback_data="catalog")
    builder.button(text="🔍Категории товаров", callback_data="categories")
    builder.button(text="🛒Корзина", callback_data="cart")
    builder.button(text="📥 Мои заказы", callback_data="my_orders")
    builder.button(text="✅Оформить заказ", callback_data="order")

    if user_chat_id in ADMIN_CHATS:
        builder.button(text="⚙️Админ-панель", callback_data="admin_panel")

    builder.adjust(1)
    return builder.as_markup()
