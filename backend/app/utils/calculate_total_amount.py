from sqlalchemy import select, func

from models.associations import order_product
from models.product import Product


def calculate_total_amount_expression():
    """Возвращает SQL-выражение для вычисления общей суммы заказа."""
    return select(
        func.coalesce(
            select(func.sum(Product.price))
            .select_from(order_product.join(Product))
            .where(order_product.c.order_id == order_product.c.order_id)
            .correlate_except(Product)
            .scalar_subquery(),
            0
        )
    ).scalar_subquery()
