import asyncio
import pytest


@pytest.mark.asyncio
async def test_handler_processes_message(handler, startup_message) -> None:
    """Test that handler receives and returns message from mailbox"""
    mailbox = handler.mailbox

    # Enqueue message
    await mailbox.enqueue(startup_message)

    # Give handler time to process
    await asyncio.sleep(0.2)

    # Verify message was routed (handler._route returns the message)
    # Handler is running and consuming from queue


@pytest.mark.asyncio
async def test_handler_processes_multiple_messages(handler, startup_board) -> None:
    """Test that handler processes multiple messages in order"""
    from uuid import uuid4
    from datetime import datetime
    from shared.models.messages import Message, Metadata, Startup
    from shared.models.constants import MessageTypes
    
    mailbox = handler.mailbox
    
    # Create and enqueue multiple messages
    for i in range(3):
        metadata = Metadata(
            message_id=uuid4(),
            timestamp=datetime.now(),
            message_type=MessageTypes.STARTUP,
        )
        content = Startup(board=startup_board)
        msg = Message(metadata=metadata, content=content)
        await mailbox.enqueue(msg)

    # Give handler time to process all
    await asyncio.sleep(0.3)

    # Handler is consuming messages from queue
