from itertools import combinations
from shared.models.messages import Cell, RBCCells


class Algorithms:

    def _candidate_options(self, cells: tuple[Cell, ...]) -> tuple[int, ...]:
        return tuple(sorted(set().union(*(c.candidates for c in cells))))

    def _candidate_single(self, cells: RBCCells) -> RBCCells:
        updates = {
            c.id: c.model_copy(update={"value": c.candidates[0]})
            for c in cells.cells
            if c.value is None and c.candidates is not None and len(c.candidates) == 1
        }
        return self._updated_rbc(cells, updates)

    def _candidate_union(self, cells: tuple[Cell, ...]) -> set[int]:
        return set().union(*(c.candidates for c in cells))

    def _candidate_update(self, cells: RBCCells) -> RBCCells:
        candidates = self._candidate_values(cells)
        updates = {
            c.id: c.model_copy(update={"candidates": candidates})
            for c in cells.cells
            if c.value is None
        }
        return self._updated_rbc(cells, updates)

    def _candidate_values(self, cells: RBCCells) -> tuple[int, ...]:
        used = {c.value for c in cells.cells if c.value is not None}
        return tuple(v for v in range(1, 10) if v not in used)


    def _hidden_updates(self, cells: RBCCells, size: int) -> dict[object, Cell]:
        updates: dict[object, Cell] = {}
        unsolved = self._unsolved_cells(cells)
        options = self._candidate_options(unsolved)
        for candidates in combinations(options, size):
            affected = tuple(
                cell
                for cell in unsolved
                if any(c in cell.candidates for c in candidates)
            )
            if len(affected) != size:
                continue
            candidate_set = set(candidates)
            for cell in affected:
                reduced = tuple(c for c in cell.candidates if c in candidate_set)
                if reduced != cell.candidates:
                    updates[cell.id] = cell.model_copy(update={"candidates": reduced})
        return updates

    def _naked_updates(self, cells: RBCCells, size: int) -> dict[object, Cell]:
        updates: dict[object, Cell] = {}
        unsolved = self._unsolved_cells(cells)
        for candidates in combinations(unsolved, size):
            candidate_set = self._candidate_union(candidates)
            if len(candidate_set) != size:
                continue
            candidate_ids = {c.id for c in candidates}
            for cell in unsolved:
                if cell.id in candidate_ids:
                    continue
                reduced = tuple(c for c in cell.candidates if c not in candidate_set)
                if reduced != cell.candidates:
                    updates[cell.id] = cell.model_copy(update={"candidates": reduced})
        return updates

    def _unsolved_cells(self, cells: RBCCells) -> tuple[Cell, ...]:
        return tuple(
            c for c in cells.cells if c.value is None and c.candidates is not None
        )

    def _updated_rbc(self, cells: RBCCells, updates: dict[object, Cell]) -> RBCCells:
        if updates == {}:
            return cells
        return cells.model_copy(
            update={"cells": tuple(updates.get(c.id, c) for c in cells.cells)}
        )

    def hidden(self, cells: RBCCells, size: int) -> RBCCells:
        c_cells = self._candidate_update(cells)
        u_cells = self._updated_rbc(c_cells, self._hidden_updates(c_cells, size))
        return self._candidate_single(u_cells)

    def naked(self, cells: RBCCells, size: int) -> RBCCells:
        c_cells = self._candidate_update(cells)
        u_cells = self._updated_rbc(c_cells, self._naked_updates(c_cells, size))
        return self._candidate_single(u_cells)

