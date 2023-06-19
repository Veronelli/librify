from uuid import uuid3
from pydantic import UUID4, BaseModel
from bson import ObjectId


class UserBase(BaseModel):
    username: str
    email: str

class User(UserBase):
    id: UUID4
    is_active: bool

    class Config:
        json_encoders = {ObjectId: str}