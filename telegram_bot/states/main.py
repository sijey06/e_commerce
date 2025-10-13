from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    main = State()                     # Главное меню
    products = State()                 # Меню товаров
    product_detail = State()           # Меню просмотра товара
    categories = State()               # Меню категорий
    category_detail = State()          # Меню детального просмотра категории
    item_cart = State()                # Меню корзины
    edit_cart = State()                # Меню редактирования корзины
    edit_cart_product = State()        # Меню редактирования товара в корзине
    change_quantity = State()          # Меню изменения количества товара
    orders = State()
    my_orders = State()                   # Меню заказов
    confirm_order = State()
    confirmation = State()            # Меню оформления заказа
    profile = State()                  # Личный кабинет
    edit_first_name = State()          # Меню редактирования имени
    edit_address = State()              # Меню редактирования адреса
    edit_phone_number = State()        # Меню редактирования номера телефона
