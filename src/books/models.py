from dataclasses import Field
from pydantic import UUID4, BaseModel
from bson import ObjectId

class BooksBase(BaseModel):
    name:str = Field(...)
    pages:int = Field(...)
    author:str = Field(...)
    year:int = Field(...)
    description:str = Field(...)
    category:str = Field(...)

class Book(BooksBase):
    id:UUID4 = Field(..., alias="_id", default_factory=UUID4)

    class Config:
        orm_mode = True
        json_encoders = {

        }
