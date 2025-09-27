import asyncio

from aiogram import F

from app import bot, dp
from commands.start import CommandStart, cmd_start
from handlers.admin import admin_panel_handler
from handlers.back import NavigationHandlers
from handlers.cart import add_to_cart
from handlers.menu import handle_main_menu_buttons
from handlers.product import show_product_details

# Создание экземпляра класса обработчиков навигации
nav_handlers = NavigationHandlers(dp)
nav_handlers.register()

dp.message.register(cmd_start, CommandStart())
dp.callback_query.register(admin_panel_handler, F.data == "admin_panel")
dp.callback_query.register(add_to_cart, F.data.contains("addtocart_"))
dp.callback_query.register(
    handle_main_menu_buttons,
    F.data.in_(["catalog", "categories", "cart", "order"]))
dp.callback_query.register(show_product_details, F.data.contains("product_"))


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
