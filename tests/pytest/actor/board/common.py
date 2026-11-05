import pytest
from helpers.board import ALL, candidate_board, check_candidates
from actors.actor_tasks.board.algorithms import common


@pytest.mark.parametrize(
    ("coordinate", "expected"),
    (((1, 1), False), ((1, 9), True), ((9, 1), True), ((2, 2), True), ((5, 5), False)),
)
def test_sees(startup_board, coordinate, expected):
    cells = {(cell.row, cell.column): cell for cell in startup_board.cells}
    assert common.sees(cells[1, 1], cells[coordinate]) is expected


def test_peers_and_cell_map(startup_board):
    source = startup_board.cells[0]
    expected = {
        (row, column)
        for row in range(1, 10)
        for column in range(1, 10)
        if (row == 1 or column == 1 or (row <= 3 and column <= 3))
        and (row, column) != (1, 1)
    }
    assert {
        (cell.row, cell.column) for cell in common.peers(startup_board, source)
    } == expected
    assert common.cell_map(startup_board) == {
        cell.id: cell for cell in startup_board.cells
    }


def test_candidates(startup_board):
    assert common.candidates(startup_board.cells[0]) == set()
    board = candidate_board({(1, 1): (1, 3, 5)})
    assert common.candidates(board.cells[0]) == {1, 3, 5}


def test_remove_candidates():
    board = candidate_board({(1, 1): (1, 3, 5)})
    check_candidates(
        lambda value: common.remove(value, {board.cells[0].id: {1, 5}}),
        board,
        {(1, 1): (3,)},
    )


@pytest.mark.parametrize("removals", (set(), {2, 4}))
def test_remove_absent_candidates(removals):
    board = candidate_board({(1, 1): (1, 3, 5)})
    result = check_candidates(
        lambda value: common.remove(value, {board.cells[0].id: removals}), board, {}
    )
    assert result is board


def test_remove_preserves_cells_without_candidates(startup_board):
    result = check_candidates(
        lambda value: common.remove(value, {startup_board.cells[0].id: set(ALL)}),
        startup_board,
        {},
    )
    assert result is startup_board