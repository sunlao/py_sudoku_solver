from collections import defaultdict
from actors.actor_tasks.board.algorithms.common import candidates, remove
from shared.models.constants import CellIds
from shared.models.messages import Board


class Intersection:

    def pointing(self, board: Board) -> Board:
        removals: dict[CellIds, set[int]] = defaultdict(set)
        for box in range(1, 10):
            box_cells = tuple(
                cell for cell in board.cells if cell.box == box and cell.value is None
            )
            for candidate in range(1, 10):
                cells = tuple(
                    cell for cell in box_cells if candidate in candidates(cell)
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
                            and candidate in candidates(cell)
                        ):
                            removals[cell.id].add(candidate)
                columns = {cell.column for cell in cells}
                if len(columns) == 1:
                    column = next(iter(columns))
                    for cell in board.cells:
                        if (
                            cell.column == column
                            and cell.box != box
                            and candidate in candidates(cell)
                        ):
                            removals[cell.id].add(candidate)
        return remove(board, removals)

    def box_line(self, board: Board) -> Board:
        removals: dict[CellIds, set[int]] = defaultdict(set)
        for candidate in range(1, 10):
            for row in range(1, 10):
                cells = tuple(
                    cell
                    for cell in board.cells
                    if cell.row == row and candidate in candidates(cell)
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
                            and candidate in candidates(cell)
                        ):
                            removals[cell.id].add(candidate)
            for column in range(1, 10):
                cells = tuple(
                    cell
                    for cell in board.cells
                    if cell.column == column and candidate in candidates(cell)
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
                            and candidate in candidates(cell)
                        ):
                            removals[cell.id].add(candidate)
        return remove(board, removals)
