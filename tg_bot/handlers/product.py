from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import dp
from api_client import fetch
from config import FAST_API_BASE_URL


# Обработчик детализированного просмотра продукта
@dp.callback_query(F.data.contains("product_"))
async def show_product_details(callback_query: CallbackQuery):
    if not isinstance(callback_query.message, Message):
        return
    if (callback_query.data is None or
            not callback_query.data.startswith('product_')):
        await callback_query.answer("Некорректные данные запроса.",
                                    show_alert=True)
        return
    product_id_str = callback_query.data.split('_')[1]
    try:
        product_id = int(product_id_str)
    except ValueError:
        await callback_query.answer("Неверный формат идентификатора продукта.",
                                    show_alert=True)
        return
    product_url = f"{FAST_API_BASE_URL}/products/{product_id}"
    product = await fetch(product_url)

    details_keyboard = InlineKeyboardBuilder()
    details_keyboard.button(text="👍Добавить в корзину",
                            callback_data=f"addtocart_{product_id}")
    details_keyboard.button(text="↩️Назад", callback_data="back_to_catalog")
    details_keyboard.adjust(1)

    await callback_query.message.edit_text(
        f"""
Название: {product['name']}
Описание: {product['description']}
Цена: {product['price']} Руб.
""",
        reply_markup=details_keyboard.as_markup()
        )
