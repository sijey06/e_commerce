from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const, Format

from config.settings import API_URL
from handlers.item_cart import CartService
from handlers.orders import OrderService
from handlers.users import UserService
from states.main import MainSG

user_service = UserService(API_URL)
cart_service = CartService(API_URL)
order_service = OrderService(API_URL, user_service, cart_service)

order_confirmation_window = Window(
    Format("""
🛍️ Оформление заказа:

🧑‍🤝‍🧑 Данные пользователя:
🖋 Имя: {user[first_name]}
🏠 Адрес доставки: {user[address]}
📞 Контактный телефон: {user[phone_number]}

🛠️ Товары в корзине:

{item_list}

💳 Общая стоимость заказа: {total_price:.2f} ₽
"""),
    Column(
        Button(Const("✅ Подтвердить заказ"), id="confirm_order",
               on_click=order_service.confirm_order_handler),
        Button(Const("↩️ Назад в корзину"), id="back_to_cart",
               on_click=lambda c, b, m: m.switch_to(MainSG.item_cart))
    ),
    getter=order_service.order_confirmation_getter,
    state=MainSG.confirm_order
)

# Окно подтверждения заказа
confirmation_window = Window(
    Const("Ваш заказ создан! Спасибо за покупку."),
    Column(
        Button(Const("Закрыть"), id="close",
               on_click=lambda c, b, m: m.switch_to(MainSG.main))
    ),
    state=MainSG.confirmation
)

# Окно с историей заказов
my_orders_window = Window(
    Format("""
📦 История заказов:

{orders}
"""),
    Column(
        Button(Const("↩️ Назад в профиль"), id="back_to_profile",
               on_click=lambda c, b, m: m.switch_to(MainSG.profile))
    ),
    getter=order_service.my_orders_getter,
    state=MainSG.my_orders
)
