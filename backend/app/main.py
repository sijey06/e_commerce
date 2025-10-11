from fastapi import FastAPI
from sqladmin import Admin

from database import engine
from admin import (UserAdmin, ProductAdmin, OrderAdmin,
                   CartItemAdmin, CategoryAdmin)
from routers import cart, category, order, product, user

# Создание экземпляра FastAPI
app = FastAPI(
    title="Интернет-магазин E-Commerce",
    description="REST API для интернет-магазина E-Commerce",
    version="1.0.0"
)


# Подключение всех маршрутизаторов
app.include_router(product.router)
app.include_router(category.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(user.router)

admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
admin.add_view(OrderAdmin)
admin.add_view(CartItemAdmin)
admin.add_view(CategoryAdmin)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
