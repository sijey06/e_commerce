from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    address: str
    phone_number: int
    chat_id: int


class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True
