import pytest

from helpers.data import create_board

from shared.models.board import BoardInput, RowInput
from shared.models.messages import Board


@pytest.fixture
def startup_board() -> Board:
    return create_board(
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
