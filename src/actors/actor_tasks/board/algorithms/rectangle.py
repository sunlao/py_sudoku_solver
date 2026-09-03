from itertools import combinations
from actors.actor_tasks.board.algorithms.common import candidates, remove

from shared.models.messages import Board


class Rectangle:

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
                        pair_set <= candidates(cell) for cell in rectangle
                    ):
                        continue
                    exact = tuple(
                        cell for cell in rectangle if candidates(cell) == pair_set
                    )
                    if len(exact) != 3:
                        continue
                    target = next(
                        cell
                        for cell in rectangle
                        if cell.id not in {item.id for item in exact}
                    )
                    extras = candidates(target) - pair_set
                    if not extras:
                        continue

                    return self._remove(board, {target.id: pair_set})
        return board
