from itertools import combinations
from shared.models.messages import Cell, RBCCells


class Algorithms:
    def _candidate_union(self, cells: tuple[Cell, ...]) -> set[int]:
        return set().union(*(c.candidates for c in cells))

    def _unsolved_cells(self, cells: RBCCells) -> tuple[Cell, ...]:
        return tuple(c for c in cells.cells if c.value is None and c.candidates is not None)

    def _updated_rbc(self, cells: RBCCells, updates: dict[object, Cell]) -> RBCCells:
        if updates == {}:
            return cells
        return cells.model_copy(
            update={"cells": tuple(updates.get(c.id, c) for c in cells.cells)}
        )

    def hidden_subset(self, cells: RBCCells, size: int) -> RBCCells:
        updates: dict[object, Cell] = {}
        unsolved = self._unsolved_cells(cells)
        for candidates in combinations(range(1, 10), size):
            affected = tuple(
                cell for cell in unsolved if any(c in cell.candidates for c in candidates)
            )
            if len(affected) != size:
                continue
            candidate_set = set(candidates)
            for cell in affected:
                reduced = tuple(c for c in cell.candidates if c in candidate_set)
                if reduced != cell.candidates:
                    updates[cell.id] = cell.model_copy(update={"candidates": reduced})
        return self._updated_rbc(cells, updates)

    def naked_subset(self, cells: RBCCells, size: int) -> RBCCells:
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
        return self._updated_rbc(cells, updates)
