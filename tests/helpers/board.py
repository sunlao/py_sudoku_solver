from collections.abc import Callable, Mapping
from fixtures.boards import create_board
from shared.models.board import BoardInput, RowInput
from shared.models.messages import Board

ALL = tuple(range(1, 10))
WITHOUT_ONE = tuple(range(2, 10))


def candidate_board(updates: Mapping[tuple[int, int], tuple[int, ...]]) -> Board:
    board = create_board(
        BoardInput(rows=tuple(RowInput(values=(None,) * 9) for _ in range(9)))
    )
    return board.model_copy(
        update={
            "cells": tuple(
                cell.model_copy(
                    update={"candidates": updates.get((cell.row, cell.column), ALL)}
                )
                for cell in board.cells
            )
        }
    )


def check_candidates(
    algorithm: Callable[[Board], Board],
    board: Board,
    changes: Mapping[tuple[int, int], tuple[int, ...]],
) -> Board:
    snapshot = board.model_dump()
    expected = board.model_copy(
        update={
            "cells": tuple(
                (
                    cell.model_copy(
                        update={"candidates": changes[(cell.row, cell.column)]}
                    )
                    if (cell.row, cell.column) in changes
                    else cell
                )
                for cell in board.cells
            )
        }
    )
    result = algorithm(board)
    assert board.model_dump() == snapshot
    assert result == expected
    return result