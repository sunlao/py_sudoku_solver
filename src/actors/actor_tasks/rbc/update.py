from datetime import datetime
from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from actors.actor_tasks.rbc.helpers.evaluate import Evaluate
from actors.actor_tasks.rbc.helpers.send import Send
from shared.models.constants import ActorDomainStatus, ActorNames
from shared.models.messages import Message, Cell, RBCCells
from shared.models.side_effects import ActorSideEffects


class Update:
    def __init__(self) -> None:
        self.evaluate = Evaluate()
        self.send = Send()

    @staticmethod
    def _already_completed(cell_cnt: int) -> bool:
        if len(cell_cnt) == 0:
            print("NoOp-Already-Completed")
            return True
        return False

    @staticmethod
    def _no_candidates(new_cell: Cell) -> bool:
        if new_cell.candidates is None:
            print("NoOp-No-Candidates")
            return True
        return False

    @staticmethod
    def _no_candidates_change(update_cell: Cell, old_cell: Cell) -> bool:
        if update_cell == old_cell:
            print("NoOp-No-Candidates-Change")
            return True
        return False

    @staticmethod
    def _no_cell_change(new_cell: Cell, old_cell: Cell) -> bool:
        if new_cell == old_cell or old_cell.value is not None:
            print("NoOp-No-Cell-Change")
            return True
        return False

    @staticmethod
    async def _send_message(
        side_effects: ActorSideEffects,
        actor: ActorNames,
        status: ActorDomainStatus,
        director_now: datetime,
    ):
        msg = xform_update_state_msg(
            sending_actor=actor,
            sending_status=status,
            last_director_timestamp=director_now,
            rbc_flag=True,
        )
        await send_update_msg(side_effects, msg)

    @staticmethod
    def _set_state_completed(
        side_effects: ActorSideEffects,
        dto: Message[Cell],
        new_cell: Cell,
        rbc_old: RBCCells,
    ) -> bool:
        if new_cell.value is not None:
            rbc_update = rbc_old.model_copy(
                update={
                    "cells": tuple(
                        new_cell if c.id == new_cell.id else c for c in rbc_old.cells
                    )
                }
            )
            side_effects.state.set_rbc_cell(dto, rbc_update)
            print("Set-State-Completed")
            return True
        return False

    @staticmethod
    def _update_cell_candidates(old_cell, new_cell):
        if old_cell.candidates is None:
            candidates = new_cell.candidates
        else:
            candidates = tuple(
                sorted(set(old_cell.candidates) & set(new_cell.candidates))
            )
        return old_cell.model_copy(update={"candidates": candidates})

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[Cell]
    ) -> None:
        director_now = side_effects.now()
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        rbc_old = side_effects.state.get_cache(dto)
        cell_cnt = [c for c in rbc_old.cells if c.value is None]
        new_cell = dto.content
        old_cell = next(c for c in rbc_old.cells if c.id == new_cell.id)
        if (
            self._already_completed(cell_cnt) is True
            or self._no_cell_change(new_cell, old_cell) is True
            or self._set_state_completed(side_effects, dto, new_cell, rbc_old) is True
            or self._no_candidates(new_cell) is True
        ):
            return
        update_cell = self._update_cell_candidates(old_cell, new_cell)
        if self._no_candidates_change(update_cell, old_cell) is True:
            return
        rbc_update = rbc_old.model_copy(
            update={
                "cells": tuple(
                    update_cell if c.id == update_cell.id else c for c in rbc_old.cells
                )
            }
        )
        rbc_cells = await self.evaluate.all(side_effects, rbc_update)
        side_effects.state.set_rbc_cell(dto, rbc_cells)
        await self.send.rbcs(side_effects, dto, rbc_old, rbc_cells)
        await self._send_message(
            side_effects, actor, ActorDomainStatus.WORKING, director_now
        )
        print(f"**director rbc:update end {dto.metadata.actor_behavior}")
