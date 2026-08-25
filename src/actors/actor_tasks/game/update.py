from shared.models.messages import Cell, Message
from shared.models.side_effects import ActorSideEffects

class Update:
    def __init__(self) -> None:
        pass

    def update_cell(self) -> None:
        pass

    def set_board_cell(self) -> None:
        pass

    def send_update_process(self) -> None:
        pass

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[Cell]
    ) -> None: