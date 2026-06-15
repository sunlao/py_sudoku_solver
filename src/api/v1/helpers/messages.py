from shared.models.messages import Board, Message, Metadata, Startup
from shared.models.constants import Behavior


def start_up(board: Board) -> Message:
    metadata = Metadata(message_type=Behavior.STARTUP)
    content = Startup(board=board)
    return Message(metadata=metadata, content=content)
