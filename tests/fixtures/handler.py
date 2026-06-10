import asyncio
import pytest
from typing import AsyncGenerator
from actors.handler import Handler
from actors.mailbox import Mailbox


@pytest.fixture
async def handler(
    mailbox: Mailbox, test_mailbox: Mailbox
) -> AsyncGenerator[Handler, None]:
    """Create and start a handler"""
    handler = Handler(
        mailbox=mailbox,
        test=test_mailbox,
    )
    task = handler.start()
    yield handler
    handler.stop()
    await asyncio.sleep(0.1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
