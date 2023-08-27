from bson import ObjectId
from pydantic import BaseModel


class BookBaseModel(BaseModel):
    name: str
    autor: ObjectId
    publisher: ObjectId
    description: str


class BookOutput(BookBaseModel):
    readers: list[ObjectId]
    calification: int
