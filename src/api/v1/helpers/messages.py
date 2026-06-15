from api.v1.helpers.client import client
from shared.models.messages import Board, MessageSend, Metadata, Startup
from shared.models.constants import MessageTypes


def start_up(board: Board) -> MessageSend:
    metadata = Metadata(message_type=MessageTypes.STARTUP)
    content = Startup(board=board)
    return MessageSend(metadata=metadata, content=content)
