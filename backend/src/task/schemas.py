"""Request and response bodies for the task routes.

FastAPI checks every request body against one of these classes before it calls the route
function. If the body does not match, FastAPI responds with a 422 error by itself. See
https://fastapi.tiangolo.com/tutorial/body/ for more info.

MongoDB names the ID field "_id", but Pydantic does not allow field names that start with
an underscore, so the field is called "id" in Python and "_id" in JSON (its alias).
"""

from datetime import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Fields that every task request and response has, with the same type."""

    title: str = Field(min_length=1)
    description: str | None = None
    isChecked: bool = False


class TaskCreate(TaskBase):
    """Body of POST /api/task."""


class TaskUpdate(TaskCreate):
    """Body of PUT /api/task/{task_id}, which replaces the whole task.

    _id is only used to check that it matches the ID in the URL, so exclude=True leaves it
    out of model_dump().
    """

    id: str = Field(alias="_id", exclude=True)
    dateCreated: datetime


class TaskResponse(TaskBase):
    """A task as returned by the API."""

    id: str = Field(alias="_id")
    dateCreated: datetime
