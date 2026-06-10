import asyncio
import pytest
from datetime import datetime
from uuid import uuid4
from shared.models.messages import Message, MessageMetadata, StartupMessage
from shared.models.constants import MessageTypes
from actors.mailbox import Mailbox


@pytest.fixture
def startup_message() -> Message[StartupMessage]:
    """Create a test startup message"""
    metadata = MessageMetadata(
        message_id=str(uuid4()),
        timestamp=datetime.now(),
        message_type=MessageTypes.STARTUP,
    )
    content = StartupMessage(actor_type="controller")
    return Message(metadata=metadata, content=content)


@pytest.mark.asyncio
async def test_mailbox_enqueue_dequeue(startup_message: Message[StartupMessage]) -> None:
    """Test that messages can be enqueued and dequeued from mailbox in FIFO order"""
    mailbox: Mailbox[Message[StartupMessage]] = Mailbox()

    # Enqueue message
    await mailbox.enqueue(startup_message)
    assert mailbox.size() == 1

    # Dequeue message
    dequeued = await mailbox.dequeue()
    assert dequeued.metadata.message_id == startup_message.metadata.message_id
    assert dequeued.content.actor_type == startup_message.content.actor_type
    assert mailbox.size() == 0


@pytest.mark.asyncio
async def test_mailbox_fifo_order() -> None:
    """Test that mailbox maintains FIFO order"""
    mailbox: Mailbox[Message[StartupMessage]] = Mailbox()
    messages = []

    # Create and enqueue multiple messages
    for i in range(3):
        metadata = MessageMetadata(
            message_id=f"msg-{i}",
            timestamp=datetime.now(),
            message_type=MessageTypes.STARTUP,
        )
        content = StartupMessage(actor_type=f"actor-{i}")
        msg = Message(metadata=metadata, content=content)
        messages.append(msg)
        await mailbox.enqueue(msg)

    # Dequeue and verify order
    for i, original_msg in enumerate(messages):
        dequeued = await mailbox.dequeue()
        assert dequeued.metadata.message_id == original_msg.metadata.message_id
        assert dequeued.content.actor_type == f"actor-{i}"


@pytest.mark.asyncio
async def test_mailbox_blocks_on_empty() -> None:
    """Test that dequeue blocks when mailbox is empty"""
    mailbox: Mailbox[Message[StartupMessage]] = Mailbox()

    # Create a dequeue task that should block
    dequeue_task = asyncio.create_task(mailbox.dequeue())

    # Give it time to start blocking
    await asyncio.sleep(0.1)
    assert not dequeue_task.done()

    # Enqueue a message
    metadata = MessageMetadata(
        message_id="test",
        timestamp=datetime.now(),
        message_type=MessageTypes.STARTUP,
    )
    content = StartupMessage(actor_type="test")
    msg = Message(metadata=metadata, content=content)
    await mailbox.enqueue(msg)

    # Now the task should complete
    result = await asyncio.wait_for(dequeue_task, timeout=1.0)
    assert result.metadata.message_id == "test"
