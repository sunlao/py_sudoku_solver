from contextlib import asynccontextmanager
from httpx import ASGITransport, AsyncClient


@asynccontextmanager
async def client(app):
    transport = ASGITransport(app=app)
    base = "http://pss-api:80"
    async with AsyncClient(transport=transport, base_url=base, timeout=10) as client:
        yield client
