from dataclasses import Field
from pydantic import BaseModel


class BooksBase(BaseModel):
    name:str = Field(...)
    pages:int = Field(...)
    author:str = Field(...)
    year:int = Field(...)
    description:str = Field(...)
    category:str = Field(...)

