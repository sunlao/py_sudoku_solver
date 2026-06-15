from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from httpx import ASGITransport


@asynccontextmanager
async def client(app, async_client):
    transport = ASGITransport(app=app)
    base = "http://pss-api:80"
    async with async_client(
        transport=transport, base_url=base, timeout=10
    ) as api_client:
        yield api_client
