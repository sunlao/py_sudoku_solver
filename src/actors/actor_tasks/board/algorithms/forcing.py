from collections import defaultdict, deque
from actors.actor_tasks.board.algorithms.common import (
    candidates as com_candicandidates,
    cell_map,
    peers,
    remove,
)
from shared.models.constants import CellIds
from shared.models.messages import Board, Cell


class Forcing:

    def _assume(self, board: Board, assumed: Cell, value: int) -> Board | None:
        candidates: dict[CellIds, set[int]] = {
            cell.id: com_candicandidates(cell)
            for cell in board.cells
            if cell.value is None and cell.candidates is not None
        }
        candidates[assumed.id] = {value}
        queue = deque([assumed.id])
        cells = cell_map(board)
        while queue:
            solved_id = queue.popleft()
            solved_candidates = candidates.get(solved_id)
            if solved_candidates is None or len(solved_candidates) != 1:
                continue
            solved_value = next(iter(solved_candidates))
            solved_cell = cells[solved_id]
            for peer in peers(board, solved_cell):
                peer_candidates = candidates.get(peer.id)
                if peer_candidates is None or solved_value not in peer_candidates:
                    continue
                if len(peer_candidates) == 1:
                    return None
                update = peer_candidates - {solved_value}
                if not update:
                    return None
                candidates[peer.id] = update
                if len(update) == 1:
                    queue.append(peer.id)
        updated_cells = []
        for cell in board.cells:
            update = candidates.get(cell.id)
            if (
                update is None
                or cell.candidates is None
                or update == set(cell.candidates)
            ):
                updated_cells.append(cell)
                continue
            updated_cells.append(
                cell.model_copy(update={"candidates": tuple(sorted(update))})
            )
        return board.model_copy(update={"cells": tuple(updated_cells)})

    def forcing_chains(self, board: Board) -> Board:
        bivalue = tuple(
            cell for cell in board.cells if len(com_candicandidates(cell)) == 2
        )
        for pivot in bivalue:
            values = tuple(com_candicandidates(pivot))
            branch_a = self._assume(board, pivot, values[0])
            branch_b = self._assume(board, pivot, values[1])
            if branch_a is None and branch_b is None:
                continue
            if branch_a is None:
                return remove(board, {pivot.id: {values[0]}})
            if branch_b is None:
                return remove(board, {pivot.id: {values[1]}})
            removals: dict[CellIds, set[int]] = defaultdict(set)
            for original, branch_a_cell, branch_b_cell in zip(
                board.cells,
                branch_a.cells,
                branch_b.cells,
                strict=True,
            ):
                original_candidates = com_candicandidates(original)
                if not original_candidates:
                    continue
                removed_a = original_candidates - com_candicandidates(branch_a_cell)
                removed_b = original_candidates - com_candicandidates(branch_b_cell)
                common = removed_a & removed_b
                if common:
                    removals[original.id].update(common)
            updated = remove(board, removals)
            if updated != board:
                return updated
        return board
