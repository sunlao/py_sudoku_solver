from shared.models.messages import Board, Message, Metadata, ControllerStartup
from shared.models.constants import ActorBehaviors


def start_up(board: Board) -> Message[ControllerStartup]:
    metadata = Metadata(actor_behavior=ActorBehaviors.CONTROLLER_START_UP)
    content = ControllerStartup(board=board)
    return Message(metadata=metadata, content=content)
