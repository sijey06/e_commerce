from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from config.settings import API_URL
from handlers.category import CategoryService
from handlers.products import product_selected
from states.main import MainSG

service = CategoryService(API_URL)

# Окно списка категорий
categories_list_window = Window(
    Const("Список категорий:"),
    Column(
        Select(
            Format("📚 {item[name]}"),
            items="categories",
            item_id_getter=lambda x: x["id"],
            on_click=service.category_selected,
            id="category_select"),
        Button(Const("↩️ В основное меню"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.main))),
    getter=service.get_list_categories,
    state=MainSG.categories
    )


# Окно списка категорий
categories_detail_window = Window(
    Const("Список товаров категории:"),
    Column(
        Select(
            Format("🎁 {item[name]}"),
            items="products",
            item_id_getter=lambda x: x["id"],
            on_click=product_selected,
            id="product_select"
        ),
        Button(Const("↩️ Назад к категориям"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.categories)),
        Button(Const("⬅️ В главное меню"), id="main_menu",
               on_click=lambda c, b, m: m.switch_to(MainSG.main))
               ),
    getter=service.get_list_detail_category,
    state=MainSG.category_detail
    )
