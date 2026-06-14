from typing import AsyncGenerator
import asyncio
import pytest
from actors.handler import Handler
from actors.mailbox import Mailbox


@pytest.fixture
async def handler_solo(
    mailbox: Mailbox, test_mailbox: Mailbox
) -> AsyncGenerator[Handler, None]:
    handler = Handler(mailbox=mailbox, test=test_mailbox)
    # emulate startup as if fastapi lifespan started it
    task = handler.start()
    try:
        yield handler
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
