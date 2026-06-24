from actors.state import State
from shared.models.messages import ControllerStartup, Message
from shared.models.side_effects import ActorSideEffects


class Start:

    def __init__(self) -> None:
        pass

    def set_board(self) -> None:
        pass

    def send_update_process(self) -> None:
        pass

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ControllerStartup]
    ) -> None:
        side_effects.state.set_game_board(dto, dto.content.board)
        print("**game controller end ")
