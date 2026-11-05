import pytest
from helpers.board import candidate_board, check_candidates
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
    check_candidates(Rectangle().unique_rectangle, board, {(2, 4): extras})


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
    assert check_candidates(Rectangle().unique_rectangle, board, {}) is board