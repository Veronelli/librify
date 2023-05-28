from pydantic import BaseModel
from bson import ObjectId


class UserBase(BaseModel):
    username: str
    email: str

class User(UserBase):
    id: ObjectId
    is_active: bool

    class Config:
        json_encoders = {ObjectId: str}