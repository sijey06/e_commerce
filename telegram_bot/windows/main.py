from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from states.main import MainSG

# Главное окно (меню)
main_window = Window(
       Const("Добро пожаловать в наш Интернет-магазин!"),
       Button(Const("📌Каталог товаров"), id="get_tasks",
              on_click=lambda c, b, m: m.switch_to(MainSG.products)),
       Button(Const("🔍Категории товаров"), id="create_task",
              on_click=lambda c, b, m: m.switch_to(MainSG.categories)),
       Button(Const("🛒Корзина"), id="item_cart",
              on_click=lambda c, b, m: m.switch_to(MainSG.item_cart)),
       Button(Const("📥 Мои заказы"), id="orders",
              on_click=lambda c, b, m: m.switch_to(MainSG.orders)),
       Button(Const("👤 Личный кабинет"), id="get_profile",
              on_click=lambda c, b, m: m.switch_to(MainSG.profile)),
       state=MainSG.main,
)
