from pydantic import BaseModel
from enums.status import Status


class OrderStatusUpdate(BaseModel):
    status: Status
