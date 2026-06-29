from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from shared.models.messages import Message, RBCStart
from shared.models.side_effects import ActorSideEffects


class Start:
    def __init__(self) -> None:
        pass

    def set_9x9(self) -> None:
        pass

    def send_update_process(self) -> None:
        pass

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[RBCStart]
    ) -> None:
        print("**director rbc:start begin")
