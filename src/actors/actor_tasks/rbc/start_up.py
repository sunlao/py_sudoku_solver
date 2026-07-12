from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from actors.actor_tasks.rbc.helpers.evaluate import Evaluate
from actors.actor_tasks.rbc.helpers.send import Send
from shared.models.constants import ActorDomainStatus
from shared.models.messages import Message, RBCCells
from shared.models.side_effects import ActorSideEffects


class StartUp:
    def __init__(self) -> None:
        self.evaluate = Evaluate()
        self.send = Send()

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[RBCCells]
    ) -> None:
        director_now = side_effects.now()
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        rbc_cells = await self.evaluate.all(side_effects, dto.content)
        side_effects.state.set_rbc_cell(dto, rbc_cells)
        await self.send.rbcs(side_effects, dto, dto.content, rbc_cells)
        msg = xform_update_state_msg(
            sending_actor=actor,
            sending_status=ActorDomainStatus.WORKING,
            last_director_timestamp=director_now,
            rbc_flag=True,
        )
        await send_update_msg(side_effects, msg)
        print(f"**director rbc:start-up end {dto.metadata.actor_behavior}")
