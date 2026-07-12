from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from actors.actor_tasks.rbc.helpers.evaluate import Evaluate
from actors.actor_tasks.rbc.helpers.send import Send
from shared.models.constants import ActorDomainStatus
from shared.models.messages import Message, Cell
from shared.models.side_effects import ActorSideEffects


class Update:
    def __init__(self) -> None:
        self.evaluate = Evaluate()
        self.send = Send()

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[Cell]
    ) -> None:
        print(f"**director rbc:update start {dto.metadata.actor_behavior}")
        director_now = side_effects.now()
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        rbc_old = side_effects.state.get_cache(dto)
        cell_cnt = [c for c in rbc_old.cells if c.value is None]
        if len(cell_cnt) == 0:
            print("NoOp-Already-Completed")
            return
        new_cell = dto.content
        old_cell = next(c for c in rbc_old.cells if c.id == new_cell.id)
        if new_cell == old_cell or old_cell.value is not None:
            print("NoOp-No-Change")
            return
        rbc_update = rbc_old.model_copy(
            update={
                "cells": tuple(
                    new_cell if c.id == new_cell.id else c for c in rbc_old.cells
                )
            }
        )
        if new_cell.value is not None:      
            side_effects.state.set_rbc_cell(dto, rbc_update)
            print("NoOp-Completed")
            return
        print(f"old_cell: {old_cell}")
        print(f"new_cell: {new_cell}")
        # rbc_cells = await self.evaluate.all(side_effects, rbc_update)
        
        # await self.send.rbcs(side_effects, dto, rbc_old, rbc_cells)
        # msg = xform_update_state_msg(
        #     sending_actor=actor,
        #     sending_status=ActorDomainStatus.WORKING,
        #     last_director_timestamp=director_now,
        #     rbc_flag=True,
        # )
        # await send_update_msg(side_effects, msg)
        # print(f"**director rbc:update end {dto.metadata.actor_behavior}")
