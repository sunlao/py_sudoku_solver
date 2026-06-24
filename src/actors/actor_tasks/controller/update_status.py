from shared.models.messages import Message, ActorDomainUpdate
from shared.models.side_effects import ActorSideEffects


class UpdateStatus:

    def __init__(self) -> None:
        pass

    def set_process(self) -> None:
        pass

    def check_solved(self) -> None:
        pass

    def send_side_effect(self) -> None:
        pass

    def send_observer(self) -> None:
        pass

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ActorDomainUpdate]
    ) -> None:
        print('**director controler:update-status end')
        print(f"end id: {dto.metadata.message_id}")
        print(f"end ab: {dto.metadata.actor_behavior}")

        print(f"start id: {dto.content.start_metadata.message_id}")
        print(f"start ab: {dto.content.start_metadata.actor_behavior}")

