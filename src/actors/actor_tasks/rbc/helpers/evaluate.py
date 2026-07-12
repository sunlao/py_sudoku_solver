from actors.actor_tasks.rbc.helpers.algorithms import Algorithms
from shared.models.messages import RBCCells, Cell
from shared.models.side_effects import ActorSideEffects


class Evaluate:
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

    async def all(self, side_effects: ActorSideEffects, cells: RBCCells) -> RBCCells:
        results = await side_effects.gather(
            side_effects.run_sync(self.algorithms.naked, cells, 1),
            side_effects.run_sync(self.algorithms.hidden, cells, 1),
            side_effects.run_sync(self.algorithms.naked, cells, 2),
            side_effects.run_sync(self.algorithms.hidden, cells, 2),
            side_effects.run_sync(self.algorithms.naked, cells, 3),
            side_effects.run_sync(self.algorithms.hidden, cells, 3),
        )
        return self._merge_rbcs(results)
