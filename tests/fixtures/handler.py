import asyncio
import pytest
from typing import AsyncGenerator
from actors.handler import Handler
from actors.mailbox import Mailbox
from fixtures.mailbox import mailbox


@pytest.fixture
async def handler(mailbox: Mailbox) -> AsyncGenerator[Handler, None]:
    """Create and start a handler"""
    test_handler = Handler(mailbox)
    task = test_handler.start()
    yield test_handler
    test_handler.stop()
    await asyncio.sleep(0.1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass