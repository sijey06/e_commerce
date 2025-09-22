from enum import Enum


class Status(str, Enum):
    NEW = "НОВЫЙ"
    IN_PROGRESS = "В ОБРАБОТКЕ"
    SENT = "ОТПРАВЛЕН"
