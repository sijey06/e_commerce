import aiohttp
from aiogram_dialog import DialogManager

from states.main import MainSG


class ProductService:
    """Сервис для работы с продуктами через REST API."""

    def __init__(self, api_url):
        self.api_url = api_url

    async def fetch_products(self, session):
        """Получает список продуктов из API."""
        async with session.get(f"{self.api_url}/products") as response:
            return await response.json()

    async def fetch_product_by_id(self, session, product_id):
        """Получает продукт по его ID из API."""
        async with session.get(
            f"{self.api_url}/products/{product_id}"
        ) as response:
            if response.status == 200:
                product = await response.json()
                return product
            return None

    async def product_selected(self, callback, select,
                               manager: DialogManager, product_id):
        """Обработчик выбора товара для просмотра."""
        manager.current_context().dialog_data["product_id"] = product_id
        await manager.switch_to(MainSG.product_detail)

    async def get_list_products(self, dialog_manager: DialogManager, **kwargs):
        """Обработчик получения списка товаров."""
        event = dialog_manager.event
        user = event.from_user if hasattr(event, 'from_user') else None
        if user is None or user.id is None:
            return {"products": []}
        async with aiohttp.ClientSession() as session:
            products = await self.fetch_products(session)
            formatted_products = [
                {
                    "id": product["id"],
                    "name": product["name"]
                }
                for product in products
            ]
        return {"products": formatted_products}

    async def product_detail_getter(self, *args, **kwargs):
        """Обработчик детального просмотра товара."""
        dialog_manager = kwargs.pop('dialog_manager', None)
        product_id = dialog_manager.current_context().dialog_data.get(
            "product_id")
        async with aiohttp.ClientSession() as session:
            product = await self.fetch_product_by_id(session, product_id)
            if product:
                return {"product": product}
        return {}
