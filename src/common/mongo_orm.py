from pymongo import MongoClient
from typing import Any
from pymongo.collection import Collection
from pymongo.results import DeleteResult
import motor.motor_asyncio

from src.config.envs import settings

MongoResponse = dict[str,Any] | list[dict[str,Any]]
Query = dict[str,Any]

class MongoDB:
    def __init__(self, host: str = 'localhost', port: int = 27017, username: str = None, password: str = None):
        """
        Initialize a MongoDB connection.

        Args:
            host (str): The MongoDB server host. Defaults to 'localhost'.
            port (int): The MongoDB server port. Defaults to 27017.
            username (str): The username for authentication. Defaults to None.
            password (str): The password for authentication. Defaults to None.
        """
        uri_with_auth = f"mongodb://{username}:{password}@{host}:{port}"
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri_with_auth)
        self.db = self.client["librify"]

    async def insert_document(self, collection_name: str, document: str) -> Any:
        """
        Insert a new document into a collection.

        Args:
            collection_name (str): The name of the collection.
            document (str): The document to be inserted.

        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        return await self.db[collection_name].insert_one(document)

    async def find_documents(self, collection_name: str, offset:int|None = None, limit:int|None=None, query: dict[str,Any]|None=None) -> list[dict[str, any]]:
        """
        Find documents in a collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (Query): The query used to filter the documents.

        Returns:
            pymongo.cursor.Cursor: A cursor to iterate over the matched documents.
        """

        cursor = self.db[collection_name].find(query)
        documents = []
        async for document in cursor:
            documents.append(document)
        return documents
        
    
    async def update_document(self, collection_name: str, query: Query, update: Any) -> Any:
        """
        Update multiple documents in a collection based on a query and an update operation.

        Args:
            collection_name (str): The name of the collection.
            query (Query): The query used to filter the documents to be updated.
            update (Any): The update operation to be applied to the matched documents.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        return await self.db[collection_name].update_one(query, {"$set": update})

    async def delete_document(self, collection_name: str, query: Query) -> DeleteResult:
        """
        Delete multiple documents from a collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (Query): The query used to filter the documents to be deleted.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        return await self.db[collection_name].delete_one(query)

    def drop_collection(self, collection_name: str) -> None:
        """
        Drop (delete) a collection.

        Args:
            collection_name (str): The name of the collection.
        """
        collection: Collection = self.db[collection_name]
        collection.drop()

def connectMongoDB():
    return MongoDB(
        host="mongodb_librify",
        username=settings.MONGO_INITDB_ROOT_USERNAME or 'root',
        password=settings.MONGO_INITDB_ROOT_PASSWORD or 'root'
        )