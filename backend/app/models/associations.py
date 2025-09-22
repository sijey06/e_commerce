from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base


# Ассоциация товаров и категорий
product_category = Table(
    "product_category",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

# Ассоциация заказов и товаров
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("product_id", Integer, ForeignKey("products.id"))
)
