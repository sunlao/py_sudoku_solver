import pytest

from helpers.board import ALL, WITHOUT_ONE, candidate_board, check_candidates

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
    check_candidates(Color().simple, candidate_board(updates), expected)


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
    check_candidates(
        Color().simple,
        candidate_board(updates),
        {
            position: WITHOUT_ONE
            for position in ((1, 1), (4, 4), (2, 2), (5, 1), (6, 1), (2, 5), (2, 6))
        },
    )


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
    check_candidates(Color().multi, candidate_board(updates), expected)


@pytest.mark.parametrize("method", ("simple", "multi"))
def test_no_coloring(method):
    board = candidate_board({})
    assert check_candidates(getattr(Color(), method), board, {}) is board