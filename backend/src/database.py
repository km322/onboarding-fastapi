"""MongoDB connection, opened and closed with the app's lifespan."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Request
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from src.config import settings

DEFAULT_DATABASE_NAME = "todoList"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Connect to MongoDB when the app starts and disconnect when it stops.

    The ping makes the app refuse to start if MongoDB is not running, after waiting at most
    5 seconds (serverSelectionTimeoutMS) for it.

    MongoDB stores dates in UTC. tz_aware=True makes PyMongo label them as UTC, so they reach
    the frontend as strings ending in "Z" (for example, "2023-09-02T01:49:32.621000Z").
    Without the "Z", browsers would read them as local time.
    """
    client: AsyncMongoClient[dict[str, Any]] = AsyncMongoClient(
        settings.MONGODB_URI, tz_aware=True, serverSelectionTimeoutMS=5000
    )
    app.state.database = client.get_default_database(default=DEFAULT_DATABASE_NAME)
    await app.state.database.command("ping")
    try:
        yield
    finally:
        await client.close()


async def get_database(request: Request) -> AsyncDatabase[dict[str, Any]]:
    """Return the app's database. Use it through the Database dependency."""
    database: AsyncDatabase[dict[str, Any]] = request.app.state.database
    return database


Database = Annotated[AsyncDatabase[dict[str, Any]], Depends(get_database)]
