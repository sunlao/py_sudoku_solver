import asyncio
import pytest
from actors.mailbox import Mailbox


@pytest.mark.asyncio
async def test_mailbox_enqueue_dequeue(startup_message) -> None:
    """Test that messages can be enqueued and dequeued from mailbox in FIFO order"""
    mailbox = Mailbox()

    # Enqueue message
    await mailbox.enqueue(startup_message)

    # Dequeue message
    dequeued = await mailbox.dequeue()
    assert dequeued.metadata.message_id == startup_message.metadata.message_id
    assert dequeued.content.board == startup_message.content.board


@pytest.mark.asyncio
async def test_mailbox_fifo_order(startup_board) -> None:
    """Test that mailbox maintains FIFO order"""
    from uuid import uuid4
    from datetime import datetime
    from shared.models.messages import Message, Metadata, Startup
    from shared.models.constants import MessageTypes
    
    mailbox = Mailbox()
    messages = []

    # Create and enqueue multiple messages
    for i in range(3):
        metadata = Metadata(
            message_id=uuid4(),
            timestamp=datetime.now(),
            message_type=MessageTypes.STARTUP,
        )
        content = Startup(board=startup_board)
        msg = Message(metadata=metadata, content=content)
        messages.append(msg)
        await mailbox.enqueue(msg)

    # Dequeue and verify order
    for i, original_msg in enumerate(messages):
        dequeued = await mailbox.dequeue()
        assert dequeued.metadata.message_id == original_msg.metadata.message_id


@pytest.mark.asyncio
async def test_mailbox_blocks_on_empty(startup_message) -> None:
    """Test that dequeue blocks when mailbox is empty"""
    mailbox = Mailbox()

    # Create a dequeue task that should block
    dequeue_task = asyncio.create_task(mailbox.dequeue())

    # Give it time to start blocking
    await asyncio.sleep(0.1)
    assert not dequeue_task.done()

    # Enqueue a message
    await mailbox.enqueue(startup_message)

    # Now the task should complete
    result = await asyncio.wait_for(dequeue_task, timeout=1.0)
    assert result.metadata.message_id == startup_message.metadata.message_id
