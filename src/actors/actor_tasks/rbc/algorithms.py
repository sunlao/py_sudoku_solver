from itertools import combinations
from shared.models.constants import CellIds
from shared.models.messages import Cell, RBCCells


class Algorithms:
    def _candidates(self, cells: tuple[Cell, ...]) -> set[int]:
        values = {c.value for c in cells if c.value is not None}
        return {v for v in range(1, 10) if v not in values}

    def _affected_ids(
        self, cells: RBCCells, candidates: set[int], size: int
    ) -> set[CellIds]:
        ids = {
            cell.id
            for cell in cells.cells
            if cell.value is None and any(c in cell.candidates for c in candidates)
        }
        if len(ids) != size:
            return set()
        return ids

    def _hidden_candidates(
        self, cell: Cell, affected_ids: set[CellIds], candidates: set[int]
    ) -> Cell:
        if cell.id not in affected_ids:
            return cell
        update = tuple(c for c in cell.candidates if c in candidates)
        if cell.candidates == update:
            return cell
        return cell.model_copy(update={"candidates": update})

    def _hidden_candidates_all(self, cells: RBCCells, size: int) -> RBCCells:
        unsolved_candidates = set().union(
            *(c.candidates for c in cells.cells if c.value is None)
        )
        for candidates in combinations(unsolved_candidates, size):
            candidates_set = set(candidates)
            ids = self._affected_ids(cells, candidates_set, size)
            if ids == set():
                continue
            hidden_candidates = tuple(
                self._hidden_candidates(c, ids, candidates_set) for c in cells.cells
            )
            if cells.cells != hidden_candidates:
                return cells.model_copy(update={"cells": hidden_candidates})
        return cells

    def _naked_candidates(
        self, cell: Cell, affected_ids: set[CellIds], candidates: set[int]
    ) -> Cell:
        if cell.id not in affected_ids:
            return cell
        update = tuple(c for c in cell.candidates if c not in candidates)
        if cell.candidates == update:
            return cell
        return cell.model_copy(update={"candidates": update})

    def _naked_candidates_all(self, cells: RBCCells, size: int) -> RBCCells:
        unsolved_cells = tuple(c for c in cells.cells if c.value is None)
        for combo_cells in combinations(unsolved_cells, size):
            candidates = set().union(*(c.candidates for c in combo_cells))
            if len(candidates) != size:
                continue
            naked_ids = {c.id for c in combo_cells}
            ids = {
                c.id
                for c in unsolved_cells
                if c.id not in naked_ids and c.candidates is not None
            }
            naked_candidates = tuple(
                self._naked_candidates(c, ids, candidates) for c in cells.cells
            )
            if cells.cells != naked_candidates:
                return cells.model_copy(update={"cells": naked_candidates})
        return cells

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

    def hidden(self, cells: RBCCells, size: int) -> RBCCells:
        u_cells = self._update_all_candidates(cells)
        h_cells = self._hidden_candidates_all(u_cells, size)
        return self._update_candidate_is_one_all(h_cells)

    def naked(self, cells: RBCCells, size: int) -> RBCCells:
        u_cells = self._update_all_candidates(cells)
        n_cells = self._naked_candidates_all(u_cells, size)
        return self._update_candidate_is_one_all(n_cells)
