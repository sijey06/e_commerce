from aiogram.filters.command import CommandStart
from aiogram.types import Message

from app import dp
from keyboards.main_keyboard import create_main_keyboard


# Обработчик старта бота
@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_chat_id = str(message.from_user.id)
    await message.answer(
        "Добро пожаловать в наш интернет-магазин!",
        reply_markup=create_main_keyboard(user_chat_id)
        )
