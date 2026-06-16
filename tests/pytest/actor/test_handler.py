import asyncio
import pytest
from shared.models.constants import ActorBehaviors


@pytest.mark.usefixtures("handler_solo")
async def test_send_recieve(
    mailbox,
    test_mailbox,
    startup_message,
    startup_board,
):
    await mailbox.enqueue(startup_message)
    message = await asyncio.wait_for(
        test_mailbox.dequeue(),
        timeout=5,
    )
    assert message.metadata.actor_behavior == ActorBehaviors.CONTROLLER_START_UP
    assert message.content.board == startup_board
