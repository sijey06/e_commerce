from typing import Union

import aiohttp
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import dp
from api_client import fetch
from config import FAST_API_BASE_URL


# Обработчик добавления товара в корзину
@dp.callback_query(F.data.contains("addtocart_"))
async def add_to_cart(callback_query: CallbackQuery):
    if not isinstance(callback_query.message, Message):
        return
    if (callback_query.data is None or
            not callback_query.data.startswith('addtocart_')):
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
    chat_id = callback_query.from_user.id
    quantity = 1

    payload = {
        "product_id": product_id,
        "quantity": quantity,
        "chat_id": chat_id
    }
    print(payload)

    api_endpoint = f"{FAST_API_BASE_URL}/item-cart/"
    async with aiohttp.ClientSession() as session:
        async with session.post(api_endpoint, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                await callback_query.answer(
                    result.get("message", "Товар успешно добавлен в корзину."))
            else:
                await callback_query.answer(
                    "Ошибка при добавлении товара в корзину.", show_alert=True)


# Добавляем обработчик кнопки "Редактировать корзину"
@dp.callback_query(F.data == "edit_cart")
async def edit_cart_handler(callback_query: CallbackQuery, state: FSMContext):
    user_chat_id = callback_query.from_user.id
    cart_url = f"{FAST_API_BASE_URL}/item-cart/{user_chat_id}"
    cart_data = await fetch(cart_url)
    cart_items = cart_data.get("cart_items", [])

    if len(cart_items) > 0:
        product_ids = [item['product_id'] for item in cart_items]
        await state.update_data(product_ids=product_ids)

        keyboard_builder = InlineKeyboardBuilder()
        for item in cart_items:
            product_url = f"{FAST_API_BASE_URL}/products/{item['product_id']}"
            product = await fetch(product_url)
            button_text = f"{product['name']} ({item['quantity']}) 📦"
            keyboard_builder.button(
                text=button_text,
                callback_data=f"edit_product_{item['product_id']}")
        keyboard_builder.button(text="↩️ Назад", callback_data="back_to_home")
        keyboard_builder.adjust(1)

        await callback_query.message.edit_text(
            "Выберите товар для редактирования:",
            reply_markup=keyboard_builder.as_markup()
        )
    else:
        await callback_query.message.answer("Ваша корзина пуста.")


# Обработчик выбора товара для редактирования
@dp.callback_query(F.data.contains("edit_product_"))
async def edit_product_handler(callback_query: CallbackQuery):
    _, raw_product_id = callback_query.data.split("_")[1:]
    try:
        product_id = int(raw_product_id)
    except ValueError:
        await callback_query.message.edit_text(
            "Неверный формат данных о товаре.")
        return
    product_url = f"{FAST_API_BASE_URL}/products/{product_id}"
    product = await fetch(product_url)
    user_chat_id = callback_query.from_user.id
    cart_url = (
        f"{FAST_API_BASE_URL}/item-cart/"
        f"{user_chat_id}?product_id={product_id}"
    )
    cart_response = await fetch(cart_url)
    cart_items = cart_response.get("cart_items", [])
    found_item = next(
        (item for item in cart_items if item.get("product_id") == product_id),
        None)
    if found_item:
        quantity_in_cart = found_item.get("quantity", 0)
    else:
        quantity_in_cart = 0

    if product is None or 'name' not in product or 'price' not in product:
        await callback_query.message.edit_text(
            "Товар временно недоступен или произошла ошибка.")
        return
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="🔄 Изменить количество",
                            callback_data=f"change_qty_{product_id}")
    keyboard_builder.button(text="❌ Удалить товар",
                            callback_data=f"remove_product_{product_id}")
    keyboard_builder.button(text="↩️ Назад", callback_data="back_to_home")
    keyboard_builder.adjust(1)

    await callback_query.message.edit_text(
        f"Товар: {product['name']}\n"
        f"Количество: {quantity_in_cart}\n"
        f"Цена: {product['price']} руб.\n\n"
        f"Выполнить действие?",
        reply_markup=keyboard_builder.as_markup()
    )


# Обработчик изменения количества товара
@dp.callback_query(F.data.contains("change_qty_"))
async def change_quantity_handler(callback_query: CallbackQuery,
                                  state: FSMContext):
    _, product_id = callback_query.data.split("_")[1:]
    await callback_query.message.answer("Введите новое количество товара:")
    await state.update_data(changing_product_id=product_id)


# Обработчик удаления товара
@dp.callback_query(F.data.contains("remove_product_"))
async def remove_product_handler(callback_query: CallbackQuery):
    _, product_id = callback_query.data.split("_")[1:]
    chat_id = callback_query.from_user.id

    api_endpoint = f"{FAST_API_BASE_URL}/item-cart/{chat_id}/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.delete(api_endpoint) as response:
            if response.status == 200:
                await callback_query.message.answer(
                    "Товар успешно удалён из корзины.")
                await show_cart(callback_query.message, chat_id)
            else:
                await callback_query.message.answer(
                    "Ошибка при удалении товара.")


# Обработчик ввода нового количества товара
@dp.message(lambda m: m.text.isdigit())
async def process_new_quantity(message: Message, state: FSMContext):
    new_quantity = int(message.text)
    product_id = (await state.get_data()).get("changing_product_id")
    chat_id = message.from_user.id
    payload = {"quantity": new_quantity}
    api_endpoint = f"{FAST_API_BASE_URL}/item-cart/{chat_id}/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.put(api_endpoint, json=payload) as response:
            if response.status == 200:
                await message.answer("Количество товара успешно обновлено.")
                await show_cart(message, chat_id)
            else:
                await message.answer("Ошибка при изменении количества товара.")
    await state.clear()


# Вспомогательная функция обработчика корзины
async def show_cart(message: Union[Message, CallbackQuery], chat_id: int):
    cart_url = f"{FAST_API_BASE_URL}/item-cart/{chat_id}"
    cart_data = await fetch(cart_url)
    cart_items = cart_data.get("cart_items", [])
    total_amount = cart_data.get("grand_total", 0)

    if len(cart_items) > 0:
        cart_list = []
        for item in cart_items:
            product_url = f"{FAST_API_BASE_URL}/products/{item['product_id']}"
            product = await fetch(product_url)
            cart_list.append(f"""
- Товар: {product['name']},
количество: {item['quantity']},
сумма: {item['total_price']} руб.
""")

        cart_keyboard = InlineKeyboardBuilder()
        cart_keyboard.button(text="✅ Заказать", callback_data="order")
        cart_keyboard.button(text="🖊 Редактировать корзину",
                             callback_data="edit_cart")
        cart_keyboard.button(text="↩️ Назад", callback_data="back_to_home")
        cart_keyboard.adjust(2)

        await message.answer(
            "\n".join([
                "Ваш заказ:",
                *cart_list,
                f"\nОбщая сумма заказа: {total_amount} руб."
            ]),
            reply_markup=cart_keyboard.as_markup(),
            parse_mode='HTML'
        )
    else:
        await message.answer("Ваша корзина пуста.")
