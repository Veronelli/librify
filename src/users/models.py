from pydantic import BaseModel, EmailStr, Field, validator

from bson import ObjectId
from uuid import UUID


class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    is_active: bool= Field(default=True)

class InputUser(UserBase):
    password: str = (...)

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: str = Field(alias="_id")
    password: str | None

    class Config:
        json_encoders = {ObjectId: str}

    @validator("id")
    def validate_object_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return value
