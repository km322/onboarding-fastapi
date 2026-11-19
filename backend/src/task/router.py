"""Task routes. Each function handles one HTTP method on one URL."""

from fastapi import APIRouter, status

from src.database import Database
from src.task import service
from src.task.exceptions import TaskNotFound
from src.task.schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/task/{task_id}")
async def get_task(task_id: str, database: Database) -> TaskResponse:
    """Return the task with the ID in the URL, or a 404 error if there is none.

    This is an example of a FastAPI route function (Express calls these request handlers).
    FastAPI calls it for every GET request to /api/task/{task_id} and fills in its
    parameters for us:

    - task_id is read from the {task_id} part of the URL.
    - database is a dependency. FastAPI gets it by calling get_database in src/database.py.

    FastAPI converts whatever the function returns into JSON and sends it with a 200 status.
    The return type, TaskResponse, decides which fields are sent. Raising an HTTPException,
    such as TaskNotFound, stops the function and sends an error response instead.
    """
    task = await service.get_by_id(database, task_id)
    if task is None:
        raise TaskNotFound()
    return task


@router.post("/task", status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, database: Database) -> TaskResponse:
    """Create a task from the request body and return it with a 201 status.

    data is the JSON request body. FastAPI validates it against TaskCreate before calling
    this function and responds with a 422 error if it is not valid, so this function only
    ever receives valid data.
    """
    return await service.create(database, data)


@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task(task_id: str, database: Database) -> None:
    """Delete the task with the ID in the URL, or return a 404 error if there is none."""
    if not await service.delete(database, task_id):
        raise TaskNotFound()
