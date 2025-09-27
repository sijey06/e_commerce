from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import bot
from keyboards.main_keyboard import create_main_keyboard
from api_client import fetch
from config import FAST_API_BASE_URL


class NavigationHandlers:
    def __init__(self, dispatcher):
        self.dp = dispatcher

    async def back_to_home(self, callback_query: CallbackQuery):
        """
        Обработчик кнопки "Назад" на главную страницу.
        """
        if isinstance(callback_query.message, Message):
            await callback_query.message.delete()
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text="Добро пожаловать в наш интернет-магазин!",
                reply_markup=create_main_keyboard(
                    str(callback_query.from_user.id))
            )

    async def back_to_catalog(self, callback_query: CallbackQuery):
        """
        Обработчик кнопки "Назад" в каталог товаров.
        """
        if isinstance(callback_query.message, Message):
            await callback_query.message.delete()
            products_url = f"{FAST_API_BASE_URL}/products/"
            products = await fetch(products_url)
            catalog_keyboard = InlineKeyboardBuilder()
            for product in products:
                catalog_keyboard.button(
                    text=f"{product['name']} - {product['price']} Руб.",
                    callback_data=f"product_{product['id']}"
                )
            catalog_keyboard.button(text="↩️Назад",
                                    callback_data="back_to_home")
            catalog_keyboard.adjust(2)
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text="Список товаров нашего магазина:",
                reply_markup=catalog_keyboard.as_markup()
            )

    async def back_to_categories(self, callback_query: CallbackQuery):
        """
        Обработчик кнопки "Назад" на страницу категорий.
        """
        if isinstance(callback_query.message, Message):
            categories_url = f"{FAST_API_BASE_URL}/categories/"
            categories = await fetch(categories_url)
            categories_keyboard = InlineKeyboardBuilder()
            for category in categories:
                categories_keyboard.button(
                    text=f"{category['name']}",
                    callback_data=f"category_{category['id']}"
                )
            categories_keyboard.button(text="↩️Назад",
                                       callback_data="back_to_home")
            categories_keyboard.adjust(2)
            await callback_query.message.edit_text(
                "Выберите категорию товаров:",
                reply_markup=categories_keyboard.as_markup()
            )

    def register(self):
        """
        Регистрация обработчиков.
        """
        self.dp.callback_query.register(self.back_to_home,
                                        F.data == "back_to_home")
        self.dp.callback_query.register(self.back_to_catalog,
                                        F.data == "back_to_catalog")
        self.dp.callback_query.register(self.back_to_categories,
                                        F.data == "back_to_categories")
