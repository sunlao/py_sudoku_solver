from shared.models.messages import Board, Message, Metadata, Startup
from shared.models.constants import ActorBehaviors


def start_up(board: Board) -> Message:
    metadata = Metadata(actor_behavior=ActorBehaviors.CONTROLLER_START_UP)
    content = Startup(board=board)
    return Message(metadata=metadata, content=content)
