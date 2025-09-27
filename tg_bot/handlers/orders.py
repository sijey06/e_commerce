from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import dp
from api_client import fetch
from config import FAST_API_BASE_URL


# Обработчик кнопки "Мои заказы"
@dp.callback_query(F.data == "my_orders")
async def my_orders_handler(callback_query: CallbackQuery):
    user_chat_id = callback_query.from_user.id
    orders_url = f"{FAST_API_BASE_URL}/orders/{user_chat_id}"
    orders_data = await fetch(orders_url)

    if len(orders_data) > 0:
        output_message = ["Список ваших заказов:"]
        separator = "-" * 30 + "\n"
        for order in orders_data:
            ordered_products = ', '.join([f'{p["name"]}' for p in order["ordered_products"]])
            total_sum = sum(p['price'] for p in order['ordered_products'])
            order_info = (
                f"📌 Заказ №: {order['number']}\n"
                f"✅ Статус: {order['status']}\n"
                f"🎁 Товары: {ordered_products}\n"
                f"💸 Сумма: {total_sum} руб.\n"
            )
            output_message.extend([separator, order_info])

        orders_keyboard = InlineKeyboardBuilder()
        orders_keyboard.button(text="↩️ Назад", callback_data="back_to_home")
        orders_keyboard.adjust(1)
        await callback_query.message.edit_text(
            '\n'.join(output_message),
            reply_markup=orders_keyboard.as_markup())
    else:
        empty_orders_keyboard = InlineKeyboardBuilder()
        empty_orders_keyboard.button(text="↩️ Назад",
                                     callback_data="back_to_home")
        empty_orders_keyboard.adjust(1)
        await callback_query.message.edit_text(
            "У вас пока нет заказов.",
            reply_markup=empty_orders_keyboard.as_markup())
