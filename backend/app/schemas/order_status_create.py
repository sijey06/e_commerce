from pydantic import BaseModel
from status import Status


class OrderStatusCreate(BaseModel):
    status: Status
