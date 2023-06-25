from pymongo import MongoClient
from typing import Any
from pymongo.collection import Collection
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

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
        self.client = MongoClient(host, port, username=username, password=password)
        self.db = self.client['librify']

    def insert_document(self, collection_name: str, document: str) -> InsertOneResult:
        """
        Insert a new document into a collection.

        Args:
            collection_name (str): The name of the collection.
            document (str): The document to be inserted.

        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        collection: Collection = self.db[collection_name]
        return collection.insert_one(document)

    def find_documents(self, collection_name: str, offset:int|None = None, limit:int|None=None) -> MongoResponse:
        """
        Find documents in a collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (Query): The query used to filter the documents.

        Returns:
            pymongo.cursor.Cursor: A cursor to iterate over the matched documents.
        """
        collection: Collection = self.db[collection_name]
        offset = offset or 0
        limit = limit or 10
        return collection.find().skip(offset).limit(limit)
        
    
    def find_one(self, collection_name:str, query: Query) -> MongoResponse:
        """
        Find one document in a collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (Query): The query used to filter the documents.

        Returns:
            pymongo.cursor.Cursor: A cursor to iterate over the matched documents.
        """
        collection: Collection = self.db[collection_name]
        return collection.find_one(query)

    def update_document(self, collection_name: str, query: Query, update: Any) -> UpdateResult:
        """
        Update multiple documents in a collection based on a query and an update operation.

        Args:
            collection_name (str): The name of the collection.
            query (Query): The query used to filter the documents to be updated.
            update (Any): The update operation to be applied to the matched documents.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        collection: Collection = self.db[collection_name]
        return collection.update_many(query, {"$set": update})

    def delete_document(self, collection_name: str, query: Query) -> DeleteResult:
        """
        Delete multiple documents from a collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (Query): The query used to filter the documents to be deleted.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        collection: Collection = self.db[collection_name]
        return collection.delete_many(query)

    def drop_collection(self, collection_name: str) -> None:
        """
        Drop (delete) a collection.

        Args:
            collection_name (str): The name of the collection.
        """
        collection: Collection = self.db[collection_name]
        collection.drop()