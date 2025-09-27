import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "Example")
FAST_API_BASE_URL = os.getenv("FAST_API_BASE_URL")
ADMIN_CHATS = os.getenv("ADMINS")
