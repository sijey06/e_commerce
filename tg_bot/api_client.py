import aiohttp


# Функция отправки GET-запросов к FastAPI
async def fetch(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            return data
