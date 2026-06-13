from shared.models.messages import Board, Cell
from shared.models.board import BoardInput, RowInput


class Boards:

    @staticmethod
    def _create(board_input: BoardInput) -> Board:
        cells: list[Cell] = []
        for row_num, row_input in enumerate(board_input.rows, start=1):
            for col, value in enumerate(row_input.values, start=1):
                box = ((row_num - 1) // 3) * 3 + ((col - 1) // 3) + 1
                cells.append(Cell(row=row_num, column=col, box=box, value=value))
        return Board(cells=tuple(cells))

    def start_up(self) -> Board:
        return self._create(
            BoardInput(
                rows=(
                    RowInput(values=(5, 3, None, None, 7, None, None, None, None)),
                    RowInput(values=(6, None, None, 1, 9, 5, None, None, None)),
                    RowInput(values=(None, 9, 8, None, None, None, None, 6, None)),
                    RowInput(values=(8, None, None, None, 6, None, None, None, 3)),
                    RowInput(values=(4, None, None, 8, None, 3, None, None, 1)),
                    RowInput(values=(7, None, None, None, 2, None, None, None, 6)),
                    RowInput(values=(None, 6, None, None, None, None, 2, 8, None)),
                    RowInput(values=(None, None, None, 4, 1, 9, None, None, 5)),
                    RowInput(values=(None, None, None, None, 8, None, None, 7, 9)),
                )
            )
        )
