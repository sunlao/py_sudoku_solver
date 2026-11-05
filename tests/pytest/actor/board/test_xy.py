import pytest

from helpers.data import ALL, board_with_candidates, candidate_board

from actors.actor_tasks.board.algorithms.xy import XY


def test_y_wing():
    board = candidate_board(
        {
            (2, 2): (1, 2),
            (2, 5): (1, 3),
            (5, 2): (2, 3),
            (5, 5): (3, 4, 5),
        }
    )
    snapshot = board.model_dump()

    result = XY().y_wing(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {(5, 5): (4, 5)})


@pytest.mark.parametrize("wing", ((1, 3), (2, 4)))
def test_y_wing_missing_distinct_links(wing):
    board = candidate_board({(2, 2): (1, 2), (2, 5): (1, 3), (5, 2): wing})
    snapshot = board.model_dump()

    result = XY().y_wing(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board


def test_xyz_wing():
    board = candidate_board(
        {
            (2, 2): (1, 2, 3),
            (2, 5): (1, 3),
            (3, 3): (2, 3),
            (2, 3): (3, 4, 5),
            (3, 5): (3, 4, 5),
        }
    )
    # r3c5 sees both wings but cannot see the pivot: its 3 must remain.
    snapshot = board.model_dump()

    result = XY().xyz_wing(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(
        board,
        {
            (2, 1): tuple(value for value in ALL if value != 3),
            (2, 3): (4, 5),
        },
    )


@pytest.mark.parametrize("wing", ((2, 4), (1, 3)))
def test_xyz_wing_missing_union(wing):
    board = candidate_board({(2, 2): (1, 2, 3), (2, 5): (1, 3), (3, 3): wing})
    snapshot = board.model_dump()

    result = XY().xyz_wing(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board


def test_xy_chain():
    board = candidate_board(
        {
            (1, 1): (1, 2),
            (1, 5): (2, 3),
            (5, 5): (3, 4),
            (5, 1): (1, 4),
        }
    )
    snapshot = board.model_dump()

    result = XY().xy_chain(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(
        board,
        {(row, 1): tuple(range(2, 10)) for row in range(1, 10) if row not in (1, 5)},
    )


def test_xy_chain_broken_link():
    board = candidate_board(
        {
            (1, 1): (1, 2),
            (1, 5): (2, 3),
            (5, 5): (3, 5),
            (5, 1): (1, 4),
        }
    )
    snapshot = board.model_dump()

    result = XY().xy_chain(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board


@pytest.mark.parametrize("method", ("y_wing", "xyz_wing", "xy_chain"))
def test_no_wings_or_chain(method):
    board = candidate_board({})
    snapshot = board.model_dump()

    result = getattr(XY(), method)(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board
