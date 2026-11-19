"""MongoDB queries for the tasks collection.

See https://pymongo.readthedocs.io/en/stable/api/pymongo/asynchronous/collection.html for
every query that a collection supports.
"""

from datetime import UTC, datetime
from typing import Any

from bson import ObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from src.task.schemas import TaskCreate, TaskResponse

COLLECTION_NAME = "tasks"


def _collection(database: AsyncDatabase[dict[str, Any]]) -> AsyncCollection[dict[str, Any]]:
    return database[COLLECTION_NAME]


def _to_response(document: dict[str, Any]) -> TaskResponse:
    """Convert a task document from MongoDB into a TaskResponse.

    MongoDB stores "_id" as an ObjectId, which is not valid JSON, so it becomes a string.
    """
    document["_id"] = str(document["_id"])
    return TaskResponse.model_validate(document)


async def create(database: AsyncDatabase[dict[str, Any]], data: TaskCreate) -> TaskResponse:
    """Insert a new task created now and return it with its id.

    MongoDB stores dates to the millisecond, so dateCreated is rounded down to match.
    """
    document = data.model_dump()
    now = datetime.now(UTC)
    document["dateCreated"] = now.replace(microsecond=now.microsecond // 1000 * 1000)
    result = await _collection(database).insert_one(document)
    document["_id"] = result.inserted_id
    return _to_response(document)


async def get_by_id(database: AsyncDatabase[dict[str, Any]], task_id: str) -> TaskResponse | None:
    """Return the task with task_id, or None if there is none or the id is not valid."""
    if not ObjectId.is_valid(task_id):
        return None
    document = await _collection(database).find_one({"_id": ObjectId(task_id)})
    return _to_response(document) if document else None


async def delete(database: AsyncDatabase[dict[str, Any]], task_id: str) -> bool:
    """Delete the task with task_id and return whether it existed."""
    if not ObjectId.is_valid(task_id):
        return False
    result = await _collection(database).delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count == 1
