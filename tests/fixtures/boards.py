import pytest
from shared.models.messages import Board, Row, Cell


def create_row(row_num: int, values: tuple[int | None, ...]) -> Row:
    cells = []
    for col_idx, value in enumerate(values, start=1):
        box_num = (row_num - 1) // 3 * 3 + (col_idx - 1) // 3 + 1
        cell = Cell(row=row_num, column=col_idx, box=box_num, value=value)
        cells.append(cell)
    return Row(cells=tuple(cells))


@pytest.fixture
def startup_board() -> Board:
    """Create a valid startup sudoku board"""
    row1 = create_row(1, (5, 3, None, None, 7, None, None, None, None))
    row2 = create_row(2, (6, None, None, 1, 9, 5, None, None, None))
    row3 = create_row(3, (None, 9, 8, None, None, None, None, 6, None))
    row4 = create_row(4, (8, None, None, None, 6, None, None, None, 3))
    row5 = create_row(5, (4, None, None, 8, None, 3, None, None, 1))
    row6 = create_row(6, (7, None, None, None, 2, None, None, None, 6))
    row7 = create_row(7, (None, 6, None, None, None, None, 2, 8, None))
    row8 = create_row(8, (None, None, None, 4, 1, 9, None, None, 5))
    row9 = create_row(9, (None, None, None, None, 8, None, None, 7, 9))
    return Board(rows=(row1, row2, row3, row4, row5, row6, row7, row8, row9))