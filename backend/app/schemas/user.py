from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str | None = None
    address: str | None = None
    phone_number: int | None = None
    chat_id: int


class UserResponse(UserCreate):
    id: int
    first_name: str | None = None
    address: str | None = None
    phone_number: int | None = None
    chat_id: int

    class Config:
        from_attributes = True


class UserEdit(BaseModel):
    first_name: str | None = None
    address: str | None = None
    phone_number: int | None = None
