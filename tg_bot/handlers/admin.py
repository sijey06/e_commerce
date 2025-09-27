from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import bot, dp
from config import ADMIN_CHATS


# Обработчик открытия административной панели
@dp.callback_query(F.data == "admin_panel")
async def admin_panel_handler(callback_query: CallbackQuery):
    if isinstance(callback_query.message, Message):
        user_chat_id = str(callback_query.from_user.id)
        if user_chat_id in ADMIN_CHATS:
            await callback_query.message.delete()
            admin_keyboard = (
                InlineKeyboardBuilder()
                .button(text="🧪Товары", callback_data="manage_products")
                .button(text="🗃️Заказы", callback_data="orders")
                .button(text="↩️Назад", callback_data="back_to_home")
                .adjust(1)
                .as_markup()
            )
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text="Добро пожаловать в админ-панель!",
                reply_markup=admin_keyboard
            )
        else:
            await callback_query.answer("Доступ запрещён.", show_alert=True)
