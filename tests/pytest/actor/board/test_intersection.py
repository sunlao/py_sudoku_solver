import pytest

from helpers.data import ALL, WITHOUT_ONE, board_with_candidates, candidate_board

from actors.actor_tasks.board.algorithms.intersection import Intersection


@pytest.mark.parametrize("size", (2, 3))
@pytest.mark.parametrize("transpose", (False, True))
@pytest.mark.parametrize("qualifies", (False, True))
def test_pointing(size, transpose, qualifies):
    updates = {
        (row, column): WITHOUT_ONE for row in range(1, 4) for column in range(1, 4)
    }
    updates.update({(1, column): ALL for column in range(1, size + 1)})
    if not qualifies:
        updates[2, 3] = ALL
    expected = (
        {(1, column): WITHOUT_ONE for column in range(4, 10)} if qualifies else {}
    )
    if transpose:
        updates = {(column, row): values for (row, column), values in updates.items()}
        expected = {(column, row): values for (row, column), values in expected.items()}
    board = candidate_board(updates)
    snapshot = board.model_dump()

    result = Intersection().pointing(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, expected)


@pytest.mark.parametrize("size", (2, 3))
@pytest.mark.parametrize("transpose", (False, True))
@pytest.mark.parametrize("qualifies", (False, True))
def test_box_line(size, transpose, qualifies):
    updates = {(1, column): WITHOUT_ONE for column in range(1, 10)}
    updates.update({(1, column): ALL for column in range(1, size + 1)})
    if not qualifies:
        updates[1, 4] = ALL
    expected = (
        {(row, column): WITHOUT_ONE for row in (2, 3) for column in range(1, 4)}
        if qualifies
        else {}
    )
    if transpose:
        updates = {(column, row): values for (row, column), values in updates.items()}
        expected = {(column, row): values for (row, column), values in expected.items()}
    board = candidate_board(updates)
    snapshot = board.model_dump()

    result = Intersection().box_line(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, expected)


@pytest.mark.parametrize("method", ("pointing", "box_line"))
def test_no_intersection(method):
    board = candidate_board({})
    snapshot = board.model_dump()

    result = getattr(Intersection(), method)(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board
