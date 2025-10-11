from database import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

# Ассоциация заказов и товаров
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("product_id", Integer, ForeignKey(
        "products.id", ondelete="CASCADE"))
)
