from collections import defaultdict
from itertools import combinations
from actors.actor_tasks.board.algorithms.common import (
    candidates as cell_candidates,
    remove,
    sees,
)
from shared.models.constants import CellIds
from shared.models.messages import Board, Cell


class XY:
    def y_wing(self, board: Board) -> Board:
        bivalue = tuple(cell for cell in board.cells if len(cell_candidates(cell)) == 2)
        for pivot in bivalue:
            pivot_candidates = cell_candidates(pivot)
            wings = tuple(
                cell
                for cell in bivalue
                if sees(pivot, cell)
                and len(pivot_candidates & cell_candidates(cell)) == 1
            )
            for wing_a, wing_b in combinations(wings, 2):
                candidates_a = cell_candidates(wing_a)
                candidates_b = cell_candidates(wing_b)
                shared_a = pivot_candidates & candidates_a
                shared_b = pivot_candidates & candidates_b
                if shared_a == shared_b:
                    continue
                elimination = (candidates_a & candidates_b) - pivot_candidates
                if len(elimination) != 1:
                    continue
                candidate = next(iter(elimination))
                removals: dict[CellIds, set[int]] = defaultdict(set)
                for cell in board.cells:
                    if cell.id in {pivot.id, wing_a.id, wing_b.id}:
                        continue
                    if (
                        sees(cell, wing_a)
                        and sees(cell, wing_b)
                        and candidate in cell_candidates(cell)
                    ):
                        removals[cell.id].add(candidate)
                updated = remove(board, removals)
                if updated != board:
                    return updated
        return board

    def xyz_wing(self, board: Board) -> Board:
        pivots = tuple(cell for cell in board.cells if len(cell_candidates(cell)) == 3)
        bivalue = tuple(cell for cell in board.cells if len(cell_candidates(cell)) == 2)
        for pivot in pivots:
            pivot_candidates = cell_candidates(pivot)
            wings = tuple(
                cell
                for cell in bivalue
                if sees(pivot, cell) and cell_candidates(cell) < pivot_candidates
            )
            for wing_a, wing_b in combinations(wings, 2):
                candidates_a = cell_candidates(wing_a)
                candidates_b = cell_candidates(wing_b)
                if candidates_a | candidates_b != pivot_candidates:
                    continue
                shared = candidates_a & candidates_b
                if len(shared) != 1:
                    continue
                candidate = next(iter(shared))
                removals: dict[CellIds, set[int]] = defaultdict(set)
                for cell in board.cells:
                    if cell.id in {pivot.id, wing_a.id, wing_b.id}:
                        continue
                    if (
                        sees(cell, pivot)
                        and sees(cell, wing_a)
                        and sees(cell, wing_b)
                        and candidate in cell_candidates(cell)
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
    ) -> Board | None:
        linked = tuple(
            cell
            for cell in board.cells
            if cell.id not in visited
            and len(cell_candidates(cell)) == 2
            and outgoing in cell_candidates(cell)
            and sees(current, cell)
        )
        for next_cell in linked:
            next_candidates = cell_candidates(next_cell)
            next_outgoing = next(
                candidate for candidate in next_candidates if candidate != outgoing
            )
            visited_next = visited | {next_cell.id}
            if next_outgoing == target:
                removals: dict[CellIds, set[int]] = defaultdict(set)
                for cell in board.cells:
                    if cell.id in visited_next:
                        continue
                    if (
                        target in cell_candidates(cell)
                        and sees(cell, start)
                        and sees(cell, next_cell)
                    ):
                        removals[cell.id].add(target)
                updated = remove(board, removals)
                if updated != board:
                    return updated
            updated = self._xy_chain_search(
                board,
                start,
                next_cell,
                target,
                next_outgoing,
                visited_next,
            )
            if updated is not None:
                return updated
        return None

    def xy_chain(self, board: Board) -> Board:
        starts = tuple(cell for cell in board.cells if len(cell_candidates(cell)) == 2)
        for start in starts:
            start_candidates = cell_candidates(start)
            for target in start_candidates:
                outgoing = next(
                    candidate for candidate in start_candidates if candidate != target
                )
                updated = self._xy_chain_search(
                    board,
                    start,
                    start,
                    target,
                    outgoing,
                    {start.id},
                )
                if updated is not None:
                    return updated
        return board
