import aiohttp
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from states.main import MainSG


class CartService:
    """Сервис для работы с корзиной пользователя через REST API."""

    def __init__(self, api_url):
        self.api_url = api_url

    async def add_to_cart(self, session, product_id, quantity, chat_id):
        """Добавляет товар в корзину."""
        url = f"{self.api_url}/item-cart/"
        payload = {
            "product_id": product_id,
            "quantity": quantity,
            "chat_id": chat_id
        }
        async with session.post(url, json=payload) as resp:
            return resp.status == 200

    async def fetch_cart(self, session, chat_id):
        """Получает содержимое корзины по chat_id."""
        url = f"{self.api_url}/item-cart/{chat_id}"
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            return None

    async def handle_add_to_cart(self, query: CallbackQuery,
                                 button, manager: DialogManager):
        """Обрабатывает нажатие кнопки 'Добавить в корзину'."""
        product_id = manager.current_context().dialog_data.get("product_id")
        chat_id = query.from_user.id
        async with aiohttp.ClientSession() as session:
            success = await self.add_to_cart(session, product_id, 1, chat_id)
        message = ("Товар успешно добавлен в корзину!"
                   if success else "Ошибка. Товар не добавился.")
        await query.bot.send_message(chat_id, message)
        await query.answer("")

    async def cart_getter(self, dialog_manager: DialogManager, **kwargs):
        """Возвращает список товаров в корзине."""
        chat_id = dialog_manager.event.from_user.id
        async with aiohttp.ClientSession() as session:
            cart_data = await self.fetch_cart(session, chat_id)
        return cart_data or {}

    async def get_item_cart(self, dialog_manager: DialogManager, **kwargs):
        """Форматирует список товаров в корзине."""
        cart_data = await self.cart_getter(dialog_manager)
        if not cart_data.get("cart_items"):
            return {"products": "Корзина пуста"}
        result = []
        grand_total = sum(
            [item['total_price'] for item in cart_data['cart_items']])
        for idx, item in enumerate(cart_data['cart_items'], start=1):
            category_name = item['product'].get(
                'category', {}).get('name', 'Категория неизвестна')
            formatted_item = (
                f"{idx}. ➕ {item['product']['name']}\n"
                f"📄 Описание: {item['product']['description']}\n"
                f"🛠️ Категория: {category_name}\n"
                f"📊 Кол-во: {item['quantity']}\n"
                f"💸 Цена: {item['total_price']} ₽\n"
            )
            result.append(formatted_item)
        total_line = f"💳 Общая сумма заказа: {grand_total:.2f} ₽"
        result.append(total_line)
        return {"products": "\n\n".join(result)}

    async def get_edit_cart_data(self,
                                 dialog_manager: DialogManager, **kwargs):
        """Возвращает товары в корзине для окна редактирования."""
        chat_id = dialog_manager.event.from_user.id
        async with aiohttp.ClientSession() as session:
            cart_data = await self.fetch_cart(session, chat_id)
        return {"cart_items": cart_data.get("cart_items", [])}

    async def selected_item(self, call: CallbackQuery, widget,
                            manager: DialogManager, item_id):
        """Выбирает элемент корзины для дальнейшего редактирования."""
        cart_data = await self.get_edit_cart_data(manager)
        selected_item = next(
            (i for i in cart_data["cart_items"] if i["id"] == int(item_id)),
            None)
        if not selected_item:
            raise ValueError("Элемент корзины не найден")
        manager.current_context().dialog_data[
            "current_item_id"] = str(selected_item["product"]["id"])
        await manager.switch_to(MainSG.edit_cart_product)

    async def product_detail_getter(self,
                                    dialog_manager: DialogManager, **kwargs):
        """Возвращает детализированную информацию о товаре."""
        current_item_id = dialog_manager.current_context().dialog_data.get(
            "current_item_id")
        cart_data = await self.get_edit_cart_data(dialog_manager)
        item = next(
            (i for i in cart_data[
                "cart_items"
                ] if i["product"]["id"] == int(current_item_id)), None)
        if not item:
            raise ValueError("Товар не найден")
        return {"item": item}

    async def delete_item(self, call: CallbackQuery,
                          widget, manager: DialogManager):
        """Удаляет товар из корзины."""
        chat_id = manager.event.from_user.id
        product_id = manager.current_context().dialog_data.get(
            "current_item_id")
        async with aiohttp.ClientSession() as session:
            url = f"{self.api_url}/item-cart/{chat_id}/{product_id}"
            async with session.delete(url) as resp:
                if resp.status == 200:
                    await call.message.reply(
                        "Товар успешно удалён из корзины.")
                    await manager.switch_to(MainSG.item_cart)
                else:
                    await call.message.edit_text("Ошибка при удалении товара.")

    async def change_quantity(self, call: CallbackQuery,
                              widget, manager: DialogManager):
        """Открывает форму для изменения количества товара."""
        await manager.switch_to(MainSG.change_quantity)

    async def change_quantity_submit(self, call: CallbackQuery,
                                     widget, manager: DialogManager,
                                     new_value):
        """Обновляет количество товара в корзине."""
        chat_id = call.from_user.id
        item_id = manager.current_context().dialog_data.get("current_item_id")
        cart_data = await self.get_edit_cart_data(manager)
        cart_items = cart_data.get("cart_items", [])
        current_item = next(
            (item for item in cart_items if int(item["id"]) == int(item_id)),
            None)
        product_id = current_item["product"]["id"]
        async with aiohttp.ClientSession() as session:
            url = f"{self.api_url}/item-cart/{chat_id}/{product_id}"
            async with session.put(url, json={"quantity": new_value}) as resp:
                if resp.status == 200:
                    await call.answer("Количество товара успешно изменено.")
                    await manager.switch_to(MainSG.item_cart)
                else:
                    await call.answer(
                        "Ошибка при изменении количества товара.")
