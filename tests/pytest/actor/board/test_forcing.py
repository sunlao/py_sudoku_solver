import pytest

from helpers.data import board_with_candidates, candidate_board

from actors.actor_tasks.board.algorithms.forcing import Forcing


@pytest.mark.parametrize("contradicted", (1, 2))
def test_forcing_rejects_contradictory_assumption(contradicted):
    board = candidate_board(
        {
            (1, 1): (1, 2),
            (1, 2): (contradicted, 3),
            (2, 1): (contradicted, 3),
        }
    )
    # The contradicted value at the pivot forces both peers to 3.
    # They share a box, so that assumption is impossible.
    snapshot = board.model_dump()

    result = Forcing().forcing_chains(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {(1, 1): (3 - contradicted,)})


def test_forcing_merges_common_consequence():
    board = candidate_board(
        {
            (2, 2): (1, 2),
            (2, 5): (1, 3),
            (5, 2): (2, 3),
            (5, 5): (3, 4, 5),
        }
    )
    snapshot = board.model_dump()

    result = Forcing().forcing_chains(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {(5, 5): (4, 5)})


@pytest.mark.parametrize("updates", ({}, {(1, 1): (1, 2), (5, 5): (3, 4)}))
def test_forcing_without_common_consequence(updates):
    board = candidate_board(updates)
    snapshot = board.model_dump()

    result = Forcing().forcing_chains(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board
