from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from states.main import MainSG


async def start_command(message: Message, dialog_manager: DialogManager):
    """Обработчик комманды start."""
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)
