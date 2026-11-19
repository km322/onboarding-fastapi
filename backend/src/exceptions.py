"""Exceptions shared by all domains. Each domain subclasses these in its own exceptions.py."""

from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    """An HTTPException whose status code and message are set by the subclass."""

    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = "Server error"

    def __init__(self) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL)


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad request"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Not found"
