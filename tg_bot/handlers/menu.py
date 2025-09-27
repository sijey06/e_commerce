from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import dp
from api_client import fetch
from config import FAST_API_BASE_URL


# Обработчик кнопок главного меню
@dp.callback_query(F.data.in_(["catalog", "categories", "cart", "order"]))
async def handle_main_menu_buttons(callback_query: CallbackQuery):
    action = callback_query.data
    user_chat_id = callback_query.from_user.id

    if isinstance(callback_query.message, Message):
        if action == 'catalog':
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
            catalog_keyboard.adjust(1)
            await callback_query.message.edit_text(
                "Список товаров нашего магазина:",
                reply_markup=catalog_keyboard.as_markup()
            )

        elif action == 'categories':
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
            categories_keyboard.adjust(1)
            await callback_query.message.edit_text(
                "Выберите категорию товаров:",
                reply_markup=categories_keyboard.as_markup()
            )

        elif action == 'cart':
            cart_url = f"{FAST_API_BASE_URL}/item-cart/{user_chat_id}"
            cart_data = await fetch(cart_url)
            cart_items = cart_data.get("cart_items", [])
            total_amount = cart_data.get("grand_total", 0)

            if len(cart_items) > 0:
                cart_list = []
                for item in cart_items:
                    product_url = (
                        f"{FAST_API_BASE_URL}/products/{item['product_id']}")
                    product = await fetch(product_url)
                    cart_list.append(
                        f"- Товар: {product['name']}, "
                        f"количество: {item['quantity']}, "
                        f"сумма: {item['total_price']} Руб."
                    )

                cart_keyboard = InlineKeyboardBuilder()
                cart_keyboard.button(
                    text="✅Заказать", callback_data="order")
                cart_keyboard.button(
                    text="🖊 Редактировать корзину",
                    callback_data="edit_cart")
                cart_keyboard.button(
                    text="↩️Назад", callback_data="back_to_home")
                cart_keyboard.adjust(1)

                await callback_query.message.edit_text(
                    "\n".join([
                        "Ваш заказ:",
                        *cart_list,
                        f"\nОбщая сумма заказа: {total_amount} Руб."
                    ]),
                    reply_markup=cart_keyboard.as_markup(),
                    parse_mode='HTML'
                )
            else:
                empty_cart_keyboard = InlineKeyboardBuilder()
                empty_cart_keyboard.button(text="↩️Назад",
                                           callback_data="back_to_home")
                empty_cart_keyboard.adjust(1)

                await callback_query.message.edit_text(
                    "Ваша корзина пуста.",
                    reply_markup=empty_cart_keyboard.as_markup()
                )

        elif action == 'order':
            await callback_query.message.edit_text(
                "Сейчас эта функция недоступна.",
                "Оформление заказа скоро станет доступно."
            )
