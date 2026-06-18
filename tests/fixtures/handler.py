import asyncio
import pytest
from actors.handler import Handler
from actors.static_data.read import Read
from api.v1.helpers.load_executable import load_executable
from shared.models.constants import StaticDataNames
from shared.models.side_effects import HandlerSideEffects


@pytest.fixture
async def handler_solo(mailbox, test_mailbox):
    handler = Handler(
        HandlerSideEffects(
            mailbox=mailbox,
            test_mailbox=test_mailbox,
            static_data=Read,
            create_task=asyncio.create_task,
            load_executable=load_executable,
        )
    )

    task = handler.start()

    try:
        yield handler
    finally:
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass
