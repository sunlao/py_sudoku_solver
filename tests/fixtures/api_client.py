from pytest import fixture
from httpx import AsyncClient


@fixture
async def api_client():
    test_api = "http://localhost:8080"
    async with AsyncClient(base_url=test_api, timeout=10) as client:
        yield client
