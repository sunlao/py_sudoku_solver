import pytest

from helpers.data import ALL, WITHOUT_ONE, board_with_candidates, candidate_board

from actors.actor_tasks.board.algorithms.fish import Fish


@pytest.mark.parametrize(
    "scenario",
    (
        ("x_wing", (1, 4), (2, 5), ((1, 2), (1, 5), (4, 2), (4, 5))),
        (
            "swordfish",
            (1, 4, 7),
            (2, 5, 8),
            ((1, 2), (1, 5), (4, 5), (4, 8), (7, 2), (7, 8)),
        ),
        (
            "jellyfish",
            (1, 4, 7, 9),
            (2, 5, 8, 9),
            ((1, 2), (1, 5), (4, 5), (4, 8), (7, 8), (7, 9), (9, 2), (9, 9)),
        ),
    ),
)
@pytest.mark.parametrize("transpose", (False, True))
@pytest.mark.parametrize("qualifies", (False, True))
def test_fish(scenario, transpose, qualifies):
    method, rows, columns, pattern = scenario
    updates = {(row, column): WITHOUT_ONE for row in rows for column in range(1, 10)}
    updates.update({position: ALL for position in pattern})
    if not qualifies:
        updates[rows[0], 1] = ALL
    expected = (
        {
            (row, column): WITHOUT_ONE
            for row in range(1, 10)
            if row not in rows
            for column in columns
        }
        if qualifies
        else {}
    )
    if transpose:
        updates = {(column, row): values for (row, column), values in updates.items()}
        expected = {(column, row): values for (row, column), values in expected.items()}
    board = candidate_board(updates)
    snapshot = board.model_dump()

    result = getattr(Fish(), method)(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, expected)


@pytest.mark.parametrize("method", ("x_wing", "swordfish", "jellyfish"))
def test_no_fish(method):
    board = candidate_board({})
    snapshot = board.model_dump()

    result = getattr(Fish(), method)(board)

    assert board.model_dump() == snapshot
    assert result == board_with_candidates(board, {})
    assert result is board
