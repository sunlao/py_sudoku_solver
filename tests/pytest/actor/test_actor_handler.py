import asyncio
import pytest
from datetime import datetime
from uuid import uuid4
from shared.models.messages import Message, MessageMetadata, StartupMessage
from shared.models.constants import MessageTypes
from actors.mailbox import Mailbox
from actors.handler import Handler


class TestHandler(Handler[Message[StartupMessage]]):
    """Test handler that tracks processed messages"""

    def __init__(self, mailbox: Mailbox[Message[StartupMessage]]) -> None:
        super().__init__(mailbox)
        self.processed_messages: list[Message[StartupMessage]] = []

    async def message(self, msg: Message[StartupMessage]) -> None:
        """Process message by recording it"""
        self.processed_messages.append(msg)


@pytest.mark.asyncio
async def test_handler_processes_messages() -> None:
    """Test that handler processes messages from mailbox"""
    mailbox: Mailbox[Message[StartupMessage]] = Mailbox()
    handler = TestHandler(mailbox)

    # Create test message
    metadata = MessageMetadata(
        message_id="test-1",
        timestamp=datetime.now(),
        message_type=MessageTypes.STARTUP,
    )
    content = StartupMessage(actor_type="controller")
    msg = Message(metadata=metadata, content=content)

    # Start handler task
    handler_task = handler.start()

    # Enqueue message
    await mailbox.enqueue(msg)

    # Give handler time to process
    await asyncio.sleep(0.2)

    # Stop handler
    handler.stop()
    await asyncio.sleep(0.1)

    # Verify message was processed
    assert len(handler.processed_messages) == 1
    assert handler.processed_messages[0].metadata.message_id == "test-1"


@pytest.mark.asyncio
async def test_handler_processes_multiple_messages() -> None:
    """Test that handler processes multiple messages in order"""
    mailbox: Mailbox[Message[StartupMessage]] = Mailbox()
    handler = TestHandler(mailbox)

    # Create test messages
    messages = []
    for i in range(3):
        metadata = MessageMetadata(
            message_id=f"msg-{i}",
            timestamp=datetime.now(),
            message_type=MessageTypes.STARTUP,
        )
        content = StartupMessage(actor_type=f"actor-{i}")
        msg = Message(metadata=metadata, content=content)
        messages.append(msg)

    # Start handler
    handler_task = handler.start()

    # Enqueue all messages
    for msg in messages:
        await mailbox.enqueue(msg)

    # Give handler time to process all
    await asyncio.sleep(0.3)

    # Stop handler
    handler.stop()
    await asyncio.sleep(0.1)

    # Verify all messages were processed in order
    assert len(handler.processed_messages) == 3
    for i, processed in enumerate(handler.processed_messages):
        assert processed.metadata.message_id == f"msg-{i}"
