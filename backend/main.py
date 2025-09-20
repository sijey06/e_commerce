from fastapi import FastAPI

from api.admin import app as admin_router
from api.products import app as products_router
from api.users import app as users_router

app = FastAPI(title="Интернет-магазин E-Commerce",
              description="REST API для интернет-магазина E-Commerce",
              version="1.0.0")


app.include_router(admin_router)
app.include_router(products_router)
app.include_router(users_router)
