from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from shared.models.constants import ActorDomainStatus, CellIds
from actors.actor_tasks.rbc.evaluate import Evaluate
from shared.models.messages import Message, RBCCells
from shared.models.side_effects import ActorSideEffects


class StartUp:
    def __init__(self) -> None:
        self.evaluate = Evaluate()

    def _updated_cell_ids(self, old: RBCCells, new: RBCCells) -> tuple[CellIds, ...]:
        return tuple(
            new_cell.id
            for old_cell, new_cell in zip(old.cells, new.cells, strict=True)
            if old_cell.value != new_cell.value
            or old_cell.candidates != new_cell.candidates
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[RBCCells]
    ) -> None:
        print(f"**director rbc:start-up start {dto.metadata.actor_behavior}")
        director_now = side_effects.now()
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        rbc_cells = await self.evaluate.all(side_effects, dto.content)
        side_effects.state.set_rbc_cell(dto, rbc_cells)
        # maps = side_effects.static_data(dto).rbc_cell_behavior_maps()
        # updated_cell_ids = self._updated_cell_ids(dto.content, rbc_cells)
        msg = xform_update_state_msg(
            sending_actor=actor,
            sending_status=ActorDomainStatus.WORKING,
            last_director_timestamp=director_now,
            rbc_flag=True,
        )
        await send_update_msg(side_effects, msg)
        print(f"**director rbc:start-up end {dto.metadata.actor_behavior}")
