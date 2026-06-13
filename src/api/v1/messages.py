from shared.models.messages import Board, Message, Metadata, Startup
from shared.models.constants import MessageTypes


def start_up(board: Board) -> Message:
    metadata = Metadata(message_type=MessageTypes.STARTUP)
    content = Startup(board=board)
    return Message(metadata=metadata, content=content)      
