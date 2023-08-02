from typing import Any
from pymongo.results import UpdateResult

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

    async def update_one(self, query, update, *args, **kwargs):
        users = [user async for user in self.find(query=query)]
        if users == []:
            return UpdateResult(
                raw_result={"n": 0, "nModified": 0, "ok": 0.0, "updatedExisting": False},
                acknowledged=False
            )
        return UpdateResult(
            raw_result={"n": 0, "nModified": 1, "ok": 1.0, "updatedExisting": True},
            acknowledged=True
        )