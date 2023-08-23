from typing import Any

from src.common.constants import CREDENTIALS_COLLECTION
from src.common.mongo_orm import connectMongoDB
from src.users.types import UserCredentials
from tests.unit_tests.mock_collection.user_collection import InsertOneResult


async def exist_token(query: dict[str, Any]) -> dict[str, Any]:
    db = connectMongoDB()
    token = await db.find_documents(CREDENTIALS_COLLECTION, query=query)
    return token


async def insert_user_credential(
        user_credential: UserCredentials) -> InsertOneResult:
    db = connectMongoDB()
    inserted_data = await db.insert_document(
        CREDENTIALS_COLLECTION,
        user_credential)
    return inserted_data


async def update_user(
        user_credential: UserCredentials,
        query: dict[str, Any]) -> dict[str, Any]:
    db = connectMongoDB()

    updated = await db.update_document(
        CREDENTIALS_COLLECTION,
        query,
        user_credential)

    return updated
