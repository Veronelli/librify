from typing import Any
from bson import ObjectId

from src.common.mongo_orm import MongoDB
from src.config.envs import settings


db = MongoDB(
    host="mongodb_librify",
    username=settings.MONGO_INITDB_ROOT_USERNAME,
    password=settings.MONGO_INITDB_ROOT_PASSWORD
    )



async def find_user(id: str) -> dict[str, Any]:
    """
    Find a user by their ID.

    Args:
        id (str): The ID of the user.

    Returns:
        dict[str, Any]: The user document as a dictionary.
    """
    query = {"_id": ObjectId(id)}
    users = await db.find_documents("users", query)
    for user in users:
        user["_id"] = str(user["_id"])
        return user
