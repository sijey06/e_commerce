from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from config.settings import API_URL
from handlers.item_cart import CartService
from states.main import MainSG

service = CartService(API_URL)

# Окно просмотра корзины
item_cart_window = Window(
    Format("{products}"),
    Column(
        Button(Const("🛍️ Оформить заказ"), id="create_order",
               on_click=lambda c, b, m: m.switch_to(MainSG.confirm_order)),
        Button(Const("🔄 Редактировать корзину"), id="edit_cart",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_cart)),
        Button(Const("↩️ В основное меню"), id="main_menu",
               on_click=lambda c, b, m: m.switch_to(MainSG.main))),
    getter=service.get_item_cart,
    state=MainSG.item_cart,
    )

# Окно редактирования корзины
edit_cart_window = Window(
    Const("Редактирование корзины"),
    Column(
        Select(
            Format("📍 {item[product][name]}"),
            items="cart_items",
            item_id_getter=lambda x: x["id"],
            on_click=service.selected_item,
            id="select_item"
        )),
    Button(Const("↩️ Назад"), id="back",
           on_click=lambda c, b, m: m.switch_to(MainSG.item_cart)),
    getter=service.get_edit_cart_data,
    state=MainSG.edit_cart
)

product_detail_view_window = Window(
    Format("""
🎯 Детали товара:
📌 Название: {item[product][name]}
📝 Описание: {item[product][description]}
💤 Кол-во: {item[quantity]}
💸 Цена: {item[product][price]} ₽
💥 Всего: {item[total_price]} ₽
"""),
    Column(
        Button(Const("❌ Удалить из корзины"), id="delete",
               on_click=service.delete_item),
        Button(Const("🔄 Изменить кол-во"), id="change_qty",
               on_click=service.change_quantity),
        Button(Const("↩️ Назад"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_cart))
    ),
    getter=service.product_detail_getter,
    state=MainSG.edit_cart_product
)

# Окно с формой для изменения количества товара
change_quantity_window = Window(
    Const("Введите новое количество товара:"),
    TextInput(id="new_quantity_input",
              on_success=service.change_quantity_submit),
    state=MainSG.change_quantity
)
