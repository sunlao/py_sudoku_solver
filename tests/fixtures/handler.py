from datetime import datetime, UTC
import asyncio
import pytest
from actors.handler import Handler
from actors.static_data.read import Read
from actors.state import State
from api.v1.helpers.load_executable import load_executable
from api.v1.helpers.client import transport_client
from shared.models.side_effects import HandlerSideEffects


@pytest.fixture
async def handler_solo(mailbox, test_mailbox, api_with_state):
    handler = Handler(
        HandlerSideEffects(
            mailbox=mailbox,
            test_mailbox=test_mailbox,
            static_data=Read,
            create_task=asyncio.create_task,
            load_executable=load_executable,
            transport_client=transport_client,
            fastapi_app=api_with_state,
            gather=asyncio.gather,
            run_sync=asyncio.to_thread,
            state=State(),
            now=lambda: datetime.now(UTC),
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
