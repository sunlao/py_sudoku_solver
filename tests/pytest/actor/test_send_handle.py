import asyncio
from shared.models.constants import MessageTypes


async def test_send_handle(
    mailbox, test_mailbox, startup_message, startup_board, handler
):
    await mailbox.enqueue(startup_message)

    await asyncio.sleep(0.2)
    message = await asyncio.wait_for(
        test_mailbox.dequeue(),
        timeout=0.2,
    )
    assert message.metadata.message_type == MessageTypes.STARTUP
    assert message.content.board == startup_board
