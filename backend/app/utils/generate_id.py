import uuid


def generate_unique_order_number():
    return uuid.uuid4().hex[:8].upper()
