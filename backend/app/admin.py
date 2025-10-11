from sqladmin import ModelView
from models.user import User
from models.product import Product
from models.cart import CartItem
from models.category import Category
from models.order import Order


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [User.id, User.first_name]


class ProductAdmin(ModelView, model=Product):
    name = "Товар"
    name_plural = "Товары"
    column_list = [Product.id, Product.name]


class OrderAdmin(ModelView, model=Order):
    name = "Заказ"
    name_plural = "Заказы"
    column_list = [Order.id, Order.number]


class CartItemAdmin(ModelView, model=CartItem):
    name = "Корзина пользователя"
    name_plural = "Корзины пользователей"
    column_list = [CartItem.id, CartItem.chat_id]


class CategoryAdmin(ModelView, model=Category):
    name = "Категория"
    name_plural = "Категории"
    column_list = [Category.id, Category.name]
