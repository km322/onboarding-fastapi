from src.exceptions import NotFound


class TaskNotFound(NotFound):
    DETAIL = "Task not found"
