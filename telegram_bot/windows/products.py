from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from config.settings import API_URL
from handlers.item_cart import handle_add_to_cart
from handlers.products import ProductService
from states.main import MainSG

service = ProductService(API_URL)

# Окно списка товаров
product_list_window = Window(
    Const("Список товаров:"),
    Column(
        Select(
            Format("📦 {item[name]}"),
            items="products",
            item_id_getter=lambda x: x["id"],
            on_click=service.product_selected,
            id="task_select"),
        Button(Const("↩️ В основное меню"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.main))),
    getter=service.get_list_products,
    state=MainSG.products
    )

# Окно просмотра продукта
product_detail_window = Window(
    Format("""
🎯 Описание товара:

📌 Название: {product[name]}
📝 Описание: {product[description]}
📚 Категория: {product[category][name]}
💸 Цена: {product[price]} Руб.
"""),
    Column(
        Button(Const("🛒 Добавить в корзину"), id="handle_add_to_cart",
               on_click=handle_add_to_cart),
        Button(Const("↩️ Вернуться в каталог"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.products)),
    ),
    getter=service.product_detail_getter,
    state=MainSG.product_detail,
)
