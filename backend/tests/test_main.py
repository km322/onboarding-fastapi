from collections.abc import AsyncIterator

import pytest
from httpx2 import ASGITransport, AsyncClient

from src.main import app

pytestmark = pytest.mark.anyio


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


async def test_app_serves_api_docs(client: AsyncClient) -> None:
    assert (await client.get("/docs")).status_code == 200
    assert (await client.get("/openapi.json")).status_code == 200
