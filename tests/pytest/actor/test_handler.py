import asyncio
from shared.models.constants import MessageTypes


async def test_send_recieve(
    handler_solo,
    mailbox,
    test_mailbox,
    startup_message,
    startup_board,
):
    # handler_solo fixture lifespace exist with test
    # handler_solo is not asserted
    await mailbox.enqueue(startup_message)
    message = await asyncio.wait_for(
        test_mailbox.dequeue(),
        timeout=5,
    )
    assert message.metadata.message_type == MessageTypes.STARTUP
    assert message.content.board == startup_board
    print(message.content.board)
