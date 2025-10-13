import aiohttp
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from handlers.item_cart import CartService
from handlers.users import UserService
from states.main import MainSG


class OrderService:
    """Сервис для обработки заказов."""

    def __init__(self, api_url, user_service: UserService,
                 cart_service: CartService):
        self.api_url = api_url
        self.user_service = user_service
        self.cart_service = cart_service

    async def order_confirmation_getter(self,
                                        dialog_manager: DialogManager,
                                        **kwargs):
        """
        Возвращает данные пользователя и содержимое корзины
        для окна оформления заказа.
        """
        user_data = await self.user_service.get_user(
            dialog_manager.event.from_user.id)
        chat_id = dialog_manager.event.from_user.id
        async with aiohttp.ClientSession() as session:
            cart_data = await self.cart_service.fetch_cart(session, chat_id)
        if not cart_data.get("cart_items"):
            return {"item_list": "Корзина пуста"}
        result = []
        grand_total = sum(
            [item['total_price'] for item in cart_data['cart_items']])
        for idx, item in enumerate(cart_data['cart_items'], start=1):
            formatted_item = (
                f"{idx}. ✨ {item['product']['name']}\n"
                f"📊 Количество: {item['quantity']}\n"
                f"💸 Стоимость: {item['total_price']} ₽\n"
            )
            result.append(formatted_item)
        return {
            "user": user_data,
            "item_list": "\n".join(result),
            "total_price": grand_total
        }

    async def create_order(self, dialog_manager: DialogManager):
        """Формирует и отправляет заказ на сервер."""
        user_data = await self.user_service.get_user(
            dialog_manager.event.from_user.id)
        payload = {
            "first_name": user_data["first_name"],
            "address": user_data["address"],
            "phone_number": str(user_data["phone_number"]),
            "chat_id": dialog_manager.event.from_user.id,
            "status": "НОВЫЙ"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}/orders/",
                                    json=payload) as resp:
                if resp.status == 200:
                    return True
                return False

    async def confirm_order_handler(self, query: CallbackQuery,
                                    button, manager: DialogManager):
        """Обработчик кнопки 'Подтвердить заказ'."""
        success = await self.create_order(manager)
        if success:
            await manager.switch_to(MainSG.confirmation)
        else:
            await query.answer("Ошибка при оформлении заказа.",
                               show_alert=True)

    async def fetch_orders(self, session, chat_id):
        """Получает список заказов пользователя."""
        async with session.get(f"{self.api_url}/orders/{chat_id}") as response:
            if response.status == 200:
                return await response.json()
            return []

    async def my_orders_getter(self, dialog_manager: DialogManager, **kwargs):
        """Возвращает красивую историю заказов пользователя."""
        chat_id = dialog_manager.event.from_user.id
        async with aiohttp.ClientSession() as session:
            orders = await self.fetch_orders(session, chat_id)

        if len(orders) == 0:
            return {"orders": "📂 История заказов пуста"}

        result = []
        for order in orders:
            ordered_products = order.get("ordered_products", [])
            products_list = []
            for product in ordered_products:
                product_info = (
                    f"✨ {product['name']}: 💸 {product['price']} ₽\n"
                )
                products_list.append(product_info)

            order_details = (
                f"📣 Заказ № {order['number']}\n"
                f"📝 Статус: {order['status']}\n"
                f"🛠️ Товаров: {len(ordered_products)} шт.\n"
                f"{''.join(products_list)}"
                f"💳 Сумма заказа: {order['total_amount']} ₽\n"
            )
            result.append(order_details)

        return {"orders": '\n\n'.join(result)}
