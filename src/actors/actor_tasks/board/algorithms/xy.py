from collections import defaultdict
from itertools import combinations
from actors.actor_tasks.board.algorithms.common import candidates, remove, sees
from shared.models.constants import CellIds
from shared.models.messages import Board, Cell


class XY:

    def y_wing(self, board: Board) -> Board:
        bivalue = tuple(cell for cell in board.cells if len(candidates(cell)) == 2)
        for pivot in bivalue:
            pivot_candidates = candidates(pivot)
            wings = tuple(
                cell
                for cell in bivalue
                if sees(pivot, cell) and len(pivot_candidates & candidates(cell)) == 1
            )
            for wing_a, wing_b in combinations(wings, 2):
                a = candidates(wing_a)
                b = candidates(wing_b)
                shared_a = pivot_candidates & a
                shared_b = pivot_candidates & b
                if shared_a == shared_b:
                    continue
                elimination = (a & b) - pivot_candidates
                if len(elimination) != 1:
                    continue
                candidate = next(iter(elimination))
                removals: dict[CellIds, set[int]] = defaultdict(set)
                for cell in board.cells:
                    if cell.id in {
                        pivot.id,
                        wing_a.id,
                        wing_b.id,
                    }:
                        continue
                    if (
                        sees(cell, wing_a)
                        and sees(cell, wing_b)
                        and candidate in candidates(cell)
                    ):
                        removals[cell.id].add(candidate)
                updated = remove(board, removals)
                if updated != board:
                    return updated
        return board

    def xyz_wing(self, board: Board) -> Board:
        pivots = tuple(cell for cell in board.cells if len(candidates(cell)) == 3)
        bivalue = tuple(cell for cell in board.cells if len(candidates(cell)) == 2)
        for pivot in pivots:
            pivot_candidates = candidates(pivot)
            wings = tuple(
                cell
                for cell in bivalue
                if sees(pivot, cell) and candidates(cell) < pivot_candidates
            )
            for wing_a, wing_b in combinations(wings, 2):
                a = candidates(wing_a)
                b = candidates(wing_b)
                if a | b != pivot_candidates:
                    continue
                shared = a & b
                if len(shared) != 1:
                    continue
                candidate = next(iter(shared))
                removals: dict[CellIds, set[int]] = defaultdict(set)
                for cell in board.cells:
                    if cell.id in {
                        pivot.id,
                        wing_a.id,
                        wing_b.id,
                    }:
                        continue
                    if (
                        sees(cell, pivot)
                        and sees(cell, wing_a)
                        and sees(cell, wing_b)
                        and candidate in candidates(cell)
                    ):
                        removals[cell.id].add(candidate)
                updated = remove(board, removals)
                if updated != board:
                    return updated
        return board

    def _xy_chain_search(
        self,
        board: Board,
        start: Cell,
        current: Cell,
        target: int,
        outgoing: int,
        visited: set[CellIds],
    ) -> tuple[Cell, ...] | None:
        bivalue = tuple(
            cell
            for cell in board.cells
            if cell.id not in visited
            and len(candidates(cell)) == 2
            and outgoing in candidates(cell)
            and sees(current, cell)
        )
        for next_cell in bivalue:
            candidates = candidates(next_cell)
            next_outgoing = next(
                candidate for candidate in candidates if candidate != outgoing
            )
            if next_outgoing == target and next_cell.id != start.id:
                return (next_cell,)
            result = self._xy_chain_search(
                board,
                start,
                next_cell,
                target,
                next_outgoing,
                visited | {next_cell.id},
            )
            if result is not None:
                return (next_cell,) + result
        return None

    def xy_chain(self, board: Board) -> Board:
        starts = tuple(cell for cell in board.cells if len(candidates(cell)) == 2)
        for start in starts:
            start_candidates = candidates(start)
            for target in start_candidates:
                outgoing = next(
                    candidate for candidate in start_candidates if candidate != target
                )
                chain = self._xy_chain_search(
                    board,
                    start,
                    start,
                    target,
                    outgoing,
                    {start.id},
                )
                if not chain:
                    continue
                end = chain[-1]
                removals: dict[CellIds, set[int]] = defaultdict(set)
                chain_ids = {start.id, *(c.id for c in chain)}
                for cell in board.cells:
                    if cell.id in chain_ids:
                        continue
                    if (
                        target in candidates(cell)
                        and sees(cell, start)
                        and sees(cell, end)
                    ):
                        removals[cell.id].add(target)
                updated = remove(board, removals)
                if updated != board:
                    return updated
        return board
