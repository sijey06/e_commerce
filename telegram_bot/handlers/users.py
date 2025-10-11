import aiohttp

from states.main import MainSG


class UserService:
    """Сервис для работы с пользователем через REST API."""

    def __init__(self, api_url):
        self.api_url = api_url

    async def fetch(self, endpoint, method='GET', data=None):
        """Асинхронный метод для выполнения HTTP-запросов к API."""
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f'{self.api_url}/{endpoint}',
                                       json=data) as resp:
                return await resp.json(), resp.status

    async def get_user(self, chat_id):
        """Получает данные пользователя по его chat_id."""
        user_data, _ = await self.fetch(f'user/{chat_id}')
        return user_data

    async def change_field(self, chat_id, field_name, new_value):
        """Меняет указанное поле пользователя через PATCH-запрос."""
        _, status = await self.fetch(f'user/{chat_id}',
                                     method='PATCH',
                                     data={field_name: new_value})
        return status == 200

    async def user_getter(self, *args, **kwargs):
        """Геттер получения данных пользователя."""
        dialog_manager = kwargs.pop('dialog_manager', None)
        chat_id = dialog_manager.event.from_user.id
        user_data = await self.get_user(chat_id)
        if user_data:
            return {"user": user_data}
        return {}

    async def on_edit_first_name(self, event, widget,
                                 dialog_manager, input_value):
        """Обработчик изменения имени пользователя."""
        chat_id = dialog_manager.event.from_user.id
        success = await self.change_field(chat_id, 'first_name', input_value)
        if success:
            await dialog_manager.switch_to(MainSG.profile)
        else:
            await event.answer("Ошибка при изменении имени!")

    async def on_edit_address(self, event, widget,
                              dialog_manager, input_value):
        """Обработчик изменения адреса пользователя."""
        chat_id = dialog_manager.event.from_user.id
        success = await self.change_field(chat_id, 'address', input_value)
        if success:
            await dialog_manager.switch_to(MainSG.profile)
        else:
            await event.answer("Ошибка при изменении адреса!")

    async def on_edit_phone_number(self, event, widget,
                                   dialog_manager, input_value):
        """Обработчик изменения номера телефона пользователя."""
        chat_id = dialog_manager.event.from_user.id
        success = await self.change_field(chat_id, 'phone_number', input_value)
        if success:
            await dialog_manager.switch_to(MainSG.profile)
        else:
            await event.answer("Ошибка при изменении телефона!")
