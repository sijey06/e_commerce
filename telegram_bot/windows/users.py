from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Column, Row
from aiogram_dialog.widgets.text import Const, Format

from config.settings import API_URL
from handlers.users import UserService
from states.main import MainSG

service = UserService(API_URL)

# Окно личного кабинета
profile_window = Window(
    Format("""
🧑‍🤝‍🧑 Личный кабинет:

🖋 Имя: {user[first_name]}
🏠 Адрес: {user[address]}
📞 Телефон: {user[phone_number]}
"""),
    Column(
        Button(Const("✏ Редактировать Имя"), id="edit_first_name",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_first_name)),
        Button(Const("🗺️ Редактировать Адрес"), id="edit_address",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_address)),
        Button(Const("📞 Редактировать Телефон"), id="edit_phone_number",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_phone_number)),
        Button(Const("📦 Мои заказы"), id="my_orders"),
        Button(Const("⬅️ В главное меню"), id="back_to_main",
               on_click=lambda c, b, dm: dm.back())
    ),
    getter=service.user_getter,
    state=MainSG.profile,
)

# Окно редактирования имени
edit_first_name_window = Window(
    Const("🖋 Введите новое имя:"),
    TextInput(id="new_first_name", on_success=service.on_edit_first_name),
    Row(Button(Const("Отмена"), id="cancel_edit_first_name",
               on_click=lambda c, b, m: m.back())),
    state=MainSG.edit_first_name,
)

# Окно редактирования адреса
edit_address_window = Window(
    Const("🏠 Введите новый адрес:"),
    TextInput(id="new_address", on_success=service.on_edit_address),
    Row(Button(Const("Отмена"), id="cancel_edit_address",
               on_click=lambda c, b, m: m.back())),
    state=MainSG.edit_address,
)

# Окно редактирования телефона
edit_phone_number_window = Window(
    Const("📞 Введите новый номер телефона:"),
    TextInput(id="new_phone_number", on_success=service.on_edit_phone_number),
    Row(Button(Const("Отмена"), id="cancel_edit_phone_number",
               on_click=lambda c, b, m: m.back())),
    state=MainSG.edit_phone_number,
)
