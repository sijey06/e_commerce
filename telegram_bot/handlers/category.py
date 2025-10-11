import aiohttp
from aiogram_dialog import DialogManager

from states.main import MainSG


class CategoryService:
    """Сервис для работы с категориями через REST API."""

    def __init__(self, api_url):
        self.api_url = api_url

    async def fetch_categories(self, session):
        """Получает список категорий из API."""
        async with session.get(f"{self.api_url}/categories") as response:
            return await response.json()

    async def fetch_products_by_category(self, session, category_id):
        """Получает товары определенной категории из API."""
        async with session.get(
            f"{self.api_url}/categories/{category_id}"
        ) as response:
            return await response.json()

    async def category_selected(self, callback, select,
                                manager: DialogManager, category_id):
        """Обработчик выбора категории."""
        manager.current_context().dialog_data["category_id"] = category_id
        await manager.switch_to(MainSG.category_detail)

    async def product_selected(self, callback, select,
                               manager: DialogManager, product_id):
        """Обработчик выбора товара."""
        manager.current_context().dialog_data["product_id"] = product_id
        await manager.switch_to(MainSG.product_detail)

    async def get_list_categories(self,
                                  dialog_manager: DialogManager, **kwargs):
        """Обработчик получения списка категорий."""
        event = dialog_manager.event
        user = event.from_user if hasattr(event, 'from_user') else None
        if user is None or user.id is None:
            return {"categories": []}
        async with aiohttp.ClientSession() as session:
            categories = await self.fetch_categories(session)
            formatted_products = [
                {
                    "id": category["id"],
                    "name": category["name"]
                }
                for category in categories
            ]
        return {"categories": formatted_products}

    async def get_list_detail_category(self,
                                       dialog_manager: DialogManager,
                                       **kwargs):
        """Обработчик получения списка товаров выбранной категории."""
        event = dialog_manager.event
        user = event.from_user if hasattr(event, 'from_user') else None
        if user is None or user.id is None:
            return {"products": []}
        category_id = dialog_manager.current_context().dialog_data.get(
            "category_id")
        if not category_id:
            return {"products": []}
        async with aiohttp.ClientSession() as session:
            data = await self.fetch_products_by_category(session, category_id)
            if "products" in data:
                formatted_products = [
                    {
                        "id": product["id"],
                        "name": product["name"]
                    }
                    for product in data["products"]
                ]
            else:
                formatted_products = []
        return {"products": formatted_products}
