from itertools import combinations
from shared.models.constants import CellIds
from shared.models.messages import Cell, RBCCells


class Algorithms:
    def _candidates(self, cells: tuple[Cell, ...]) -> set[int]:
        values = {c.value for c in cells if c.value is not None}
        return {v for v in range(1, 10) if v not in values}

    def _hidden_affected_ids(
        self, cells: RBCCells, candidates: set[int], size: int
    ) -> set[CellIds]:
        affected = {
            cell.id
            for cell in cells.cells
            if cell.value is None and any(c in cell.candidates for c in candidates)
        }
        if len(affected) != size:
            return set()
        return affected

    def _hidden_candidates(
        self, cell: Cell, affected_ids: set[CellIds], candidates: set[int]
    ) -> Cell:
        update = None
        if cell.id in affected_ids:
            update = tuple(c for c in cell.candidates if c in candidates)
        if cell.candidates != update:
            return cell.model_copy(update={"candidates": update})
        return cell

    def _hidden_candidates_all(self, cells: RBCCells, size: int) -> RBCCells:
        unsolved_candidates = set().union(
            *(c.candidates for c in cells.cells if c.value is None)
        )
        for candidates in combinations(unsolved_candidates, size):
            ids = self._hidden_affected_ids(cells, set(candidates), size)
            if ids == set():
                continue
            hidden_candidates = tuple(
                self._hidden_candidates(c, ids, candidates) for c in cells.cells
            )
            if cells.cells != hidden_candidates:
                return cells.model_copy(update={"cells": hidden_candidates})
        return cells

    def _naked_updates(self, cells: RBCCells, size: int) -> dict[object, Cell]:
        updates: dict[object, Cell] = {}
        unsolved_ids = {c.id for c in cells.cells if c.value is None}
        for combo in combinations(unsolved_ids, size):
            candidates = set().union(*(cell.candidates for cell in combo))
            if len(candidates) != size:
                continue
            candidate_ids = {c.id for c in combo}
            for cell in unsolved:
                if cell.id in candidate_ids:
                    continue
                reduced = tuple(c for c in cell.candidates if c not in candidates)
                if reduced != cell.candidates:
                    updates[cell.id] = cell.model_copy(update={"candidates": reduced})
        return updates

    def _update_candidate_is_one(self, cell: Cell) -> Cell:
        if cell.candidates is not None and len(cell.candidates) == 1:
            return cell.model_copy(update={"value": cell.candidates[0]})
        return cell

    def _update_candidate_is_one_all(self, cells: RBCCells) -> RBCCells:
        update = tuple(self._update_candidate_is_one(c) for c in cells.cells)
        return cells.model_copy(update={"cells": update})

    def _update_cell_candidates(self, cell: Cell, candidates: set[int]) -> Cell:
        if cell.value is not None and cell.candidates is None:
            return cell
        if cell.value is not None and cell.candidates is not None:
            return cell.model_copy(update={"candidates": None})
        if cell.value is None and cell.candidates is None:
            return cell.model_copy(update={"candidates": tuple(candidates)})
        update = tuple(c for c in cell.candidates if c in candidates)
        if cell.candidates == update:
            return cell
        return cell.model_copy(update={"candidates": update})

    def _update_all_candidates(self, cells: RBCCells) -> RBCCells:
        candidates = self._candidates(cells.cells)
        update = tuple(self._update_cell_candidates(c, candidates) for c in cells.cells)
        if cells.cells == update:
            return cells
        return cells.model_copy(update={"cells": update})

    def _update_rbc(self, cells: RBCCells, updates: dict[object, Cell]) -> RBCCells:
        if updates == {}:
            return cells
        return cells.model_copy(
            update={"cells": tuple(updates.get(c.id, c) for c in cells.cells)}
        )

    def hidden(self, cells: RBCCells, size: int) -> RBCCells:
        c_cells = self._update_all_candidates(cells)
        h_cells = self._hidden_candidates_all(c_cells, size)
        return self._update_candidate_is_one_all(h_cells)

    def naked(self, cells: RBCCells, size: int) -> RBCCells:
        c_cells = self._update_all_candidates(cells)
        n_cells = self._naked_updates(c_cells, size)
        u_cells = self._update_rbc(c_cells, n_cells)
        return self._update_candidate_is_one_all(u_cells)
