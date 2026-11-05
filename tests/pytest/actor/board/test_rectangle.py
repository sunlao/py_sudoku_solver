import pytest

from helpers.data import board_with_candidates, candidate_board

from actors.actor_tasks.board.algorithms.rectangle import Rectangle


@pytest.mark.parametrize("extras", ((3,), (3, 4)))
def test_unique_rectangle(extras):
    board = candidate_board(
        {
            (1, 1): (1, 2),
            (1, 4): (1, 2),
            (2, 1): (1, 2),
            (2, 4): (1, 2, *extras),
        }
    )
    snapshot = board.model_dump()

    result = Rectangle().unique_rectangle(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {(2, 4): extras})


@pytest.mark.parametrize(
    "updates",
    (
        {(1, 1): (1, 2), (1, 4): (1, 2), (2, 1): (1, 2, 4), (2, 4): (1, 2, 3)},
        {(1, 1): (1, 2), (1, 4): (1, 2), (4, 1): (1, 2), (4, 4): (1, 2, 3)},
        {(1, 1): (1, 2), (1, 2): (1, 2), (2, 1): (1, 2), (2, 2): (1, 2, 3)},
        {(1, 1): (1, 2), (1, 4): (1, 2), (2, 1): (1, 2), (2, 4): (1, 3)},
        {(1, 1): (1, 2), (1, 4): (1, 2), (2, 1): (1, 2), (2, 4): (1, 2)},
        {},
    ),
    ids=(
        "two-exact-corners",
        "four-boxes",
        "one-box",
        "missing-pair",
        "no-extra",
        "no-pattern",
    ),
)
def test_no_unique_rectangle(updates):
    board = candidate_board(updates)
    snapshot = board.model_dump()

    result = Rectangle().unique_rectangle(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board
