from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from shared.models.constants import ActorDomainStatus
from shared.models.messages import Message, RBCStart
from shared.models.side_effects import ActorSideEffects


class Start:

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[RBCStart]
    ) -> None:
        director_now = side_effects.now()
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        side_effects.state.set_rbc_cell(dto, dto.content.cells)
        
        msg = xform_update_state_msg(
            sending_actor=actor,
            status=ActorDomainStatus.WORKING,
            last_director_timestamp=director_now,
            rbc_flag=True,
        )
        await send_update_msg(side_effects, msg)
        print(f"**director rbc:start end {dto.metadata.actor_behavior}")
