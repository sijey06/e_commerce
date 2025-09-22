from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    first_name: str
    address: str
    phone_number: str = Field(max_length=11, min_length=11)
    chat_id: int


class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True
