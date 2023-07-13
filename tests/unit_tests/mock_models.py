from contextlib import asynccontextmanager
class AsyncIterator:
    async def __aiter__(self):
        return []
    
    async def __aenter__(self):
        return {}
    
    async def __aexit__(self):
        pass

class MockDataBaseClient:
    @asynccontextmanager
    async def AsyncIterator():
        yield []
    
    @classmethod
    async def __init__(cls):
        return await AsyncIterator() 