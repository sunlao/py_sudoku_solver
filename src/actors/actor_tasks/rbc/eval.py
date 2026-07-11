from actors.actor_tasks.rbc.algorithms import Algorithms
from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from shared.models.constants import ActorDomainStatus
from shared.models.messages import Message, RBCCells, Cell
from shared.models.side_effects import ActorSideEffects


class Eval:
    def __init__(self) -> None:
        self.algorithms = Algorithms()

    def _merge_cells(self, results: tuple[Cell, ...]) -> Cell:
        cell = results[0]
        values = {c.value for c in results if c.value is not None}
        value = next(iter(values), None)
        candidates_set = [
            set(c.candidates) for c in results if c.candidates is not None
        ]
        candidates = (
            tuple(sorted(set.intersection(*candidates_set))) if candidates_set else None
        )
        if cell.value == value and cell.candidates == candidates:
            return cell
        return cell.model_copy(update={"value": value, "candidates": candidates})

    def _merge_rbcs(self, results: list[RBCCells]) -> RBCCells:
        rbc = results[0]
        results_transposed = zip(*(r.cells for r in results), strict=True)
        cells = tuple(self._merge_cells(r) for r in results_transposed)
        if rbc.cells == cells:
            return rbc
        return rbc.model_copy(update={"cells": cells})

    async def _eval_all(
        self, side_effects: ActorSideEffects, cells: RBCCells
    ) -> RBCCells:
        results = await side_effects.gather(
            side_effects.run_sync(self.algorithms.naked, cells, 1),
            side_effects.run_sync(self.algorithms.hidden, cells, 1),
            side_effects.run_sync(self.algorithms.naked, cells, 2),
            side_effects.run_sync(self.algorithms.hidden, cells, 2),
            side_effects.run_sync(self.algorithms.naked, cells, 3),
            side_effects.run_sync(self.algorithms.hidden, cells, 3),
        )
        return self._merge_rbcs(results)

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[RBCCells]
    ) -> None:
        print(f"**director rbc:eval start {dto.metadata.actor_behavior}")
        director_now = side_effects.now()
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        cells = await self._eval_all(side_effects, dto.content)
        side_effects.state.set_rbc_cell(dto, cells)
        msg = xform_update_state_msg(
            sending_actor=actor,
            sending_status=ActorDomainStatus.WORKING,
            last_director_timestamp=director_now,
            rbc_flag=True,
        )
        await send_update_msg(side_effects, msg)
        print(f"**director rbc:eval end {dto.metadata.actor_behavior}")
