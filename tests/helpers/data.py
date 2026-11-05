from collections.abc import Mapping

from shared.models.board import BoardInput, RowInput
from shared.models.constants import ActorNames, CellIds
from shared.models.messages import Board, Cell, RBCCells

ALL = tuple(range(1, 10))
WITHOUT_ONE = tuple(range(2, 10))


def create_board(board_input: BoardInput) -> Board:
    cells: list[Cell] = []
    for row_num, row_input in enumerate(board_input.rows, start=1):
        for column, cell_value in enumerate(row_input.values, start=1):
            box = ((row_num - 1) // 3) * 3 + ((column - 1) // 3) + 1
            cells.append(
                Cell(
                    id=CellIds(f"r{row_num}c{column}"),
                    row=row_num,
                    column=column,
                    box=box,
                    value=cell_value,
                )
            )
    return Board(cells=tuple(cells))


def candidate_board(updates: Mapping[tuple[int, int], tuple[int, ...]]) -> Board:
    board = create_board(
        BoardInput(rows=tuple(RowInput(values=(None,) * 9) for _ in range(9)))
    )
    return board_with_candidates(board, updates, default=ALL)


def board_with_candidates(
    board: Board,
    updates: Mapping[tuple[int, int], tuple[int, ...]],
    default: tuple[int, ...] | None = None,
) -> Board:
    cells = tuple(
        (
            cell.model_copy(
                update={
                    "candidates": updates.get(
                        (cell.row, cell.column),
                        cell.candidates if default is None else default,
                    )
                }
            )
            if (cell.row, cell.column) in updates or default is not None
            else cell
        )
        for cell in board.cells
    )
    if cells == board.cells:
        return board
    return board.model_copy(update={"cells": cells})


def candidates(cells: RBCCells, cell_id: CellIds) -> Cell:
    return next(sorted(c.candidates) for c in cells.cells if c.id == cell_id)


def value(cells: RBCCells, cell_id: CellIds) -> Cell:
    return next(c.value for c in cells.cells if c.id == cell_id)


def cell(cells: RBCCells, cell_id: CellIds) -> Cell:
    return next(c for c in cells.cells if c.id == cell_id)


def rbc_cells(*cells: Cell) -> RBCCells:
    return RBCCells(actor=ActorNames.ROW1, cells=cells)
