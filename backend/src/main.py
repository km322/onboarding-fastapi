"""Creates the FastAPI app, which handles every request that the backend receives.

CORSMiddleware sets the "Access-Control-Allow-Origin" header on responses so the frontend,
which runs on a different origin, is allowed to call the API. See
https://fastapi.tiangolo.com/tutorial/cors/ and
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
"""

import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.database import lifespan
from src.task.router import router as task_router

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def handle_unexpected_errors(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Turn any unexpected error into a 500 response, like the error handler in Express.

    The traceback is printed in the backend terminal. Because this middleware is added
    before CORSMiddleware, the 500 response still gets the CORS header, so the frontend
    sees the real error instead of a CORS error.
    """
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Unexpected error while handling %s %s", request.method, request.url)
        return JSONResponse(
            {"detail": "Internal Server Error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
