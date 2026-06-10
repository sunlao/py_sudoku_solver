import pytest
from uuid import uuid4
from datetime import datetime
from shared.models.constants import MessageTypes
from shared.models.messages import Message, Metadata, Startup, Board


@pytest.fixture
def startup_message(startup_board: Board) -> Message:
    """Create a test startup message"""
    metadata = Metadata(
        message_id=uuid4(),
        timestamp=datetime.now(),
        message_type=MessageTypes.STARTUP,
    )

    content = Startup(board=startup_board)
    return Message(metadata=metadata, content=content)