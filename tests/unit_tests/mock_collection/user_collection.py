from typing import Any

from bson import ObjectId
from tests.unit_tests.fixtures.results.users_results import MOCKED_USERS
from tests.unit_tests.interfaces import IAsyncIOMotorClient

async def iterable(list):
    for item in list:
        yield item


class InsertOneResult():
    @property
    def inserted_id(self) -> Any:
        """The inserted document's _id."""
        return ObjectId()


class MockUserCollection(IAsyncIOMotorClient):
    
    async def insert_one(self, document, *args, **kwargs):
        return InsertOneResult()

    @classmethod
    def find(cls, query: dict[str, Any]|None=None, *args, **kwargs):
        if query:
            users = [user for user in MOCKED_USERS if user['_id'] == str(query.get('_id'))]
            return iterable(users)
        return iterable(MOCKED_USERS)

    async def delete_one(self, collection, filter, *args, **kwargs):
        pass

    async def update_one(self, collection, filter, update, *args, **kwargs):
        pass