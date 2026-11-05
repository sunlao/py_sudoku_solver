import pytest

from helpers.data import ALL, WITHOUT_ONE, board_with_candidates, candidate_board

from actors.actor_tasks.board.algorithms.color import Color


@pytest.mark.parametrize("linked", (False, True))
def test_simple_color_trap(linked):
    updates = {
        (row, column): WITHOUT_ONE
        for row in range(1, 10)
        for column in range(1, 10)
        if row in (1, 4) or column == 4
    }
    updates.update({position: ALL for position in ((1, 1), (1, 4), (4, 4), (4, 2))})
    if not linked:
        updates[7, 4] = ALL
    expected = (
        {position: WITHOUT_ONE for position in ((2, 2), (3, 2), (5, 1), (6, 1))}
        if linked
        else {}
    )
    board = candidate_board(updates)
    snapshot = board.model_dump()

    result = Color().simple(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, expected)


def test_simple_color_wrap():
    updates = {
        (row, column): WITHOUT_ONE
        for row in range(1, 10)
        for column in range(1, 10)
        if row in (1, 4) or column in (2, 4)
    }
    updates.update(
        {position: ALL for position in ((1, 1), (1, 4), (4, 4), (4, 2), (2, 2))}
    )
    board = candidate_board(updates)
    expected = {
        position: WITHOUT_ONE
        for position in ((1, 1), (4, 4), (2, 2), (5, 1), (6, 1), (2, 5), (2, 6))
    }
    snapshot = board.model_dump()

    result = Color().simple(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, expected)


@pytest.mark.parametrize("linked", (False, True))
def test_multi_color_forced_component(linked):
    updates = {
        (row, column): WITHOUT_ONE
        for row in range(1, 10)
        for column in range(1, 10)
        if row == 1 or column in (2, 5)
    }
    updates.update({position: ALL for position in ((1, 1), (1, 5), (5, 5), (2, 2))})
    updates[5 if linked else 8, 2] = ALL
    expected = {(1, 1): WITHOUT_ONE, (5, 5): WITHOUT_ONE} if linked else {}
    board = candidate_board(updates)
    snapshot = board.model_dump()

    result = Color().multi(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, expected)


@pytest.mark.parametrize("method", ("simple", "multi"))
def test_no_coloring(method):
    board = candidate_board({})
    snapshot = board.model_dump()

    result = getattr(Color(), method)(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board
