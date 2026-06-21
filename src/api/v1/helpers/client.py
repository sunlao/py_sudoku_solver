from contextlib import asynccontextmanager
from httpx import ASGITransport
from shared.models.messages import Message


@asynccontextmanager
async def transport_client(app, dto: Message):
    transport = ASGITransport(app=app)
    base = "http://pss-api:80/address/v1"
    actor, behavior = dto.metadata.actor_behavior.split(".", maxsplit=1)
    base_actor_behavior = f"{base}/{actor}/{behavior}"
    async with app.state.async_client(
        transport=transport, base_url=base_actor_behavior, timeout=10
    ) as api_client:
        yield api_client
