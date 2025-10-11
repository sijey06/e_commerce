import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import Dialog, setup_dialogs

from config.settings import TELEGRAM_TOKEN
from handlers.main import start_command
from windows.categories import categories_detail_window, categories_list_window
from windows.item_cart import (change_quantity_window, edit_cart_window,
                               item_cart_window, product_detail_view_window)
from windows.main import main_window
from windows.products import product_detail_window, product_list_window
from windows.users import (edit_address_window, edit_first_name_window,
                           edit_phone_number_window, profile_window)


async def main():
    """Запуск бота."""
    bot = Bot(TELEGRAM_TOKEN)
    storage = MemoryStorage()
    dialog = Dialog(main_window, product_list_window, product_detail_window,
                    item_cart_window, edit_cart_window, categories_list_window,
                    product_detail_view_window, change_quantity_window,
                    categories_detail_window, profile_window,
                    edit_address_window, edit_first_name_window,
                    edit_phone_number_window)
    dp = Dispatcher(storage=storage)
    dp.include_router(dialog)
    setup_dialogs(dp)
    dp.message.register(start_command, Command('start'))
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
