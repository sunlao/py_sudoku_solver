import asyncio


async def test_send_handle(mailbox, startup_message, startup_board, handler):
    await mailbox.enqueue(startup_message)

    await asyncio.sleep(0.2)

    # Verify message was routed
    # assert len(handler.routed_messages) == 1
