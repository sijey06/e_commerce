from enums.status import Status
from pydantic import BaseModel


class OrderStatusUpdate(BaseModel):
    status: Status
