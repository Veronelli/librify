from abc import ABC, abstractmethod


class IAsyncIOMotorClient(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def insert_one(self, collection, document, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def find(cls, collection=None, filter=None, *args, **kwargs):
        pass

    @abstractmethod
    async def delete_one(self, collection, filter, *args, **kwargs):
        pass

    @abstractmethod
    async def update_one(self, collection, filter, update, *args, **kwargs):
        pass
