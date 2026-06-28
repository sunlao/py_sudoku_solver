from shared.models.controller import DomainActorStatus
from shared.models.messages import Message
from shared.models.side_effects import ActorSideEffects
from shared.models.state import ActorDomainState


class UpdateStatus:

    def __init__(self) -> None:
        pass

    def set_process(self) -> None:
        pass

    def check_solved(self) -> None:
        pass

    def send_side_effect(self) -> None:
        pass

    def message_actor_status(self, dto: Message) -> None:
        return DomainActorStatus(
            message_id=dto.content.start_metadata.message_id,
            type=dto.content.start_metadata.type,
            start_time=dto.content.start_metadata.times,
            end_time=dto.metadata.timestamp,
            actor_behavior=dto.content.start_metadata.actor_behavior,
        )

    async def director(self, side_effects: ActorSideEffects, dto: Message[ActorDomainState]) -> None:
        print("**director controler:update-status start")
        director_now = side_effects.now()
        print(f"director_now: {director_now}")
        cache = side_effects.state.get_cache(dto)

        print(f"dto md-ts: {dto.metadata.timestamp}")
        print(f"dto md-ts: {dto.content.actor}")

            # if s.actor == dto.content:
            #     print(f"new state: {s}")
        # domain_actor_status = self.message_actor_status(dto)
        # cache = side_effects.state.get_cache(dto)
        # side_effects.state.set_actor_domain_states(dto, domain_actor_status)
        print("**director controler:update-status end")
