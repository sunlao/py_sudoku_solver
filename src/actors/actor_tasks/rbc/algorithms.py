from itertools import combinations
from shared.models.messages import Cell, RBCCells


class Algorithms:
    def _candidates_new(self, cells: RBCCells) -> set[int]:
        values = {c.value for c in cells.cells if c.value is not None}
        return set(v for v in range(1, 10) if v not in values)

    def _candidates_union(self, cells: tuple[Cell, ...]) -> set[int]:
        return set().union(*(c.candidates for c in cells))

    def _hidden_updates(self, cells: RBCCells, size: int) -> dict[object, Cell]:
        updates: dict[object, Cell] = {}
        unsolved = self._unsolved(cells)
        candidates = self._candidates_union(unsolved)
        for combo in combinations(candidates, size):
            affected = tuple(
                cell
                for cell in unsolved
                if any(c in cell.candidates for c in combo)
            )
            # print(f"\naffected1: {affected}")
            if len(affected) != size:
                continue
            for cell in affected:
                print(f"cell: {cell}")
                reduced = tuple(c for c in cell.candidates if c in combo)
                if reduced != cell.candidates:
                    updates[cell.id] = cell.model_copy(update={"candidates": reduced})
        print(f"updates:{updates}")        
        return updates

    def _naked_updates(self, cells: RBCCells, size: int) -> dict[object, Cell]:
        updates: dict[object, Cell] = {}
        unsolved = self._unsolved(cells)
        for combo in combinations(unsolved, size):
            candidates = self._candidates_union(combo)
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

    def _unsolved(self, cells: RBCCells) -> tuple[Cell, ...]:
        return tuple(c for c in cells.cells if c.value is None)

    def _update_candidate_is_one(self, cell: Cell) -> Cell:
        if cell.candidates is not None and len(cell.candidates) == 1:
            return cell.model_copy(update={"value": cell.candidates[0]})
        return cell

    def _update_candidate_is_one_all(self, cells: RBCCells) -> RBCCells:
        update = tuple(self._update_candidate_is_one(c) for c in cells.cells)
        return self._update_rbc_cells(cells, update)

    def _update_cell_candidates(self, cell: Cell, candidates: tuple[int, ...]) -> Cell:
        if cell.value is not None:
            return cell.model_copy(update={"candidates": None})
        if cell.candidates is None:
            return cell.model_copy(update={"candidates": tuple(candidates)})
        update = tuple(c for c in cell.candidates if c in candidates)
        return cell.model_copy(update={"candidates": update})

    def _update_all_candidates(self, cells: RBCCells) -> RBCCells:
        candidates = self._candidates_new(cells)
        update = tuple(self._update_cell_candidates(c, candidates) for c in cells.cells)
        return self._update_rbc_cells(cells, update)

    def _update_rbc_cells(self, cells: RBCCells, update: tuple[Cell, ...]) -> RBCCells:
        return cells.model_copy(update={"cells": update})

    def _update_rbc(self, cells: RBCCells, updates: dict[object, Cell]) -> RBCCells:
        if updates == {}:
            return cells
        return cells.model_copy(
            update={"cells": tuple(updates.get(c.id, c) for c in cells.cells)}
        )

    def hidden(self, cells: RBCCells, size: int) -> RBCCells:
        c_cells = self._update_all_candidates(cells)
        u_cells = self._update_rbc(c_cells, self._hidden_updates(c_cells, size))
        return self._update_candidate_is_one_all(u_cells)

    def naked(self, cells: RBCCells, size: int) -> RBCCells:
        c_cells = self._update_all_candidates(cells)
        u_cells = self._update_rbc(c_cells, self._naked_updates(c_cells, size))
        return self._update_candidate_is_one_all(u_cells)
