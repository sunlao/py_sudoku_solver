from collections import defaultdict, deque
from itertools import combinations

from shared.models.constants import CellIds
from shared.models.messages import Board, Cell


class Algorithms:

    def pointing(self, board: Board) -> Board:
        removals: dict[CellIds, set[int]] = defaultdict(set)

        for box in range(1, 10):
            box_cells = tuple(
                cell for cell in board.cells if cell.box == box and cell.value is None
            )

            for candidate in range(1, 10):
                cells = tuple(
                    cell for cell in box_cells if candidate in self._candidates(cell)
                )

                if len(cells) < 2:
                    continue

                rows = {cell.row for cell in cells}

                if len(rows) == 1:
                    row = next(iter(rows))

                    for cell in board.cells:
                        if (
                            cell.row == row
                            and cell.box != box
                            and candidate in self._candidates(cell)
                        ):
                            removals[cell.id].add(candidate)

                columns = {cell.column for cell in cells}

                if len(columns) == 1:
                    column = next(iter(columns))

                    for cell in board.cells:
                        if (
                            cell.column == column
                            and cell.box != box
                            and candidate in self._candidates(cell)
                        ):
                            removals[cell.id].add(candidate)

        return self._remove(board, removals)

    def box_line(self, board: Board) -> Board:
        removals: dict[CellIds, set[int]] = defaultdict(set)

        for candidate in range(1, 10):
            for row in range(1, 10):
                cells = tuple(
                    cell
                    for cell in board.cells
                    if cell.row == row and candidate in self._candidates(cell)
                )

                if len(cells) < 2:
                    continue

                boxes = {cell.box for cell in cells}

                if len(boxes) == 1:
                    box = next(iter(boxes))

                    for cell in board.cells:
                        if (
                            cell.box == box
                            and cell.row != row
                            and candidate in self._candidates(cell)
                        ):
                            removals[cell.id].add(candidate)

            for column in range(1, 10):
                cells = tuple(
                    cell
                    for cell in board.cells
                    if cell.column == column and candidate in self._candidates(cell)
                )

                if len(cells) < 2:
                    continue

                boxes = {cell.box for cell in cells}

                if len(boxes) == 1:
                    box = next(iter(boxes))

                    for cell in board.cells:
                        if (
                            cell.box == box
                            and cell.column != column
                            and candidate in self._candidates(cell)
                        ):
                            removals[cell.id].add(candidate)

        return self._remove(board, removals)

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
            and len(self._candidates(cell)) == 2
            and outgoing in self._candidates(cell)
            and self._sees(current, cell)
        )

        for next_cell in bivalue:
            candidates = self._candidates(next_cell)
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
        starts = tuple(cell for cell in board.cells if len(self._candidates(cell)) == 2)

        for start in starts:
            start_candidates = self._candidates(start)

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
                        target in self._candidates(cell)
                        and self._sees(cell, start)
                        and self._sees(cell, end)
                    ):
                        removals[cell.id].add(target)

                updated = self._remove(board, removals)

                if updated != board:
                    return updated

        return board

    def unique_rectangle(self, board: Board) -> Board:
        unsolved = tuple(
            cell
            for cell in board.cells
            if cell.value is None and cell.candidates is not None
        )

        for rows in combinations(range(1, 10), 2):
            for columns in combinations(range(1, 10), 2):
                rectangle = tuple(
                    cell
                    for cell in unsolved
                    if cell.row in rows and cell.column in columns
                )

                if len(rectangle) != 4:
                    continue

                if len({cell.box for cell in rectangle}) != 2:
                    continue

                for pair in combinations(range(1, 10), 2):
                    pair_set = set(pair)

                    if not all(
                        pair_set <= self._candidates(cell) for cell in rectangle
                    ):
                        continue

                    exact = tuple(
                        cell for cell in rectangle if self._candidates(cell) == pair_set
                    )

                    if len(exact) != 3:
                        continue

                    target = next(
                        cell
                        for cell in rectangle
                        if cell.id not in {c.id for c in exact}
                    )

                    extras = self._candidates(target) - pair_set

                    if not extras:
                        continue

                    return self._remove(
                        board,
                        {target.id: pair_set},
                    )

        return board

    def _assume(
        self,
        board: Board,
        assumed: Cell,
        value: int,
    ) -> Board | None:
        candidates: dict[CellIds, set[int]] = {
            cell.id: self._candidates(cell)
            for cell in board.cells
            if cell.value is None and cell.candidates is not None
        }

        candidates[assumed.id] = {value}
        queue = deque([assumed.id])
        cells = self._cell_map(board)

        while queue:
            solved_id = queue.popleft()
            solved_candidates = candidates.get(solved_id)

            if solved_candidates is None or len(solved_candidates) != 1:
                continue

            solved_value = next(iter(solved_candidates))
            solved_cell = cells[solved_id]

            for peer in self._peers(board, solved_cell):
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
            cell for cell in board.cells if len(self._candidates(cell)) == 2
        )
        for pivot in bivalue:
            values = tuple(self._candidates(pivot))
            branch_a = self._assume(board, pivot, values[0])
            branch_b = self._assume(board, pivot, values[1])
            if branch_a is None and branch_b is None:
                continue
            if branch_a is None:
                return self._remove(
                    board,
                    {pivot.id: {values[0]}},
                )
            if branch_b is None:
                return self._remove(
                    board,
                    {pivot.id: {values[1]}},
                )
            removals: dict[CellIds, set[int]] = defaultdict(set)
            for original, a, b in zip(
                board.cells,
                branch_a.cells,
                branch_b.cells,
                strict=True,
            ):
                original_candidates = self._candidates(original)
                if not original_candidates:
                    continue
                a_candidates = self._candidates(a)
                b_candidates = self._candidates(b)
                removed_a = original_candidates - a_candidates
                removed_b = original_candidates - b_candidates
                common = removed_a & removed_b
                if common:
                    removals[original.id].update(common)
            updated = self._remove(board, removals)
            if updated != board:
                return updated
        return board
