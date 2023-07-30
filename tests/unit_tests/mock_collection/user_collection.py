from tests.unit_tests.fixtures.results.users_results import MOCKED_USERS
from tests.unit_tests.interfaces import IAsyncIOMotorClient

async def iterable(n):
    for i in MOCKED_USERS:
        yield i

class MockUserCollection(IAsyncIOMotorClient):
    
    async def insert_one(self, collection, document, *args, **kwargs):
        pass

    @classmethod
    def find(cls, collection=None, filter=None, *args, **kwargs):
        return iterable(MOCKED_USERS)

    async def delete_one(self, collection, filter, *args, **kwargs):
        pass

    async def update_one(self, collection, filter, update, *args, **kwargs):
        pass