from collections.abc import Mapping
from shared.models.constants import CellIds
from shared.models.messages import Board, Cell


def candidates(cell: Cell) -> set[int]:
    return set(cell.candidates or ())


def sees(left: Cell, right: Cell) -> bool:
    return left.id != right.id and (
        left.row == right.row or left.column == right.column or left.box == right.box
    )


def cell_map(board: Board) -> dict[CellIds, Cell]:
    return {cell.id: cell for cell in board.cells}


def peers(board: Board, source: Cell) -> tuple[Cell, ...]:
    return tuple(cell for cell in board.cells if sees(source, cell))


def remove(
    board: Board,
    removals: Mapping[CellIds, set[int]],
) -> Board:
    cells = tuple(
        _remove_from_cell(cell, removals.get(cell.id, set())) for cell in board.cells
    )
    if cells == board.cells:
        return board
    return board.model_copy(update={"cells": cells})


def _remove_from_cell(cell: Cell, removals: set[int]) -> Cell:
    if cell.candidates is None or not removals:
        return cell
    candidates_new = tuple(
        candidate for candidate in cell.candidates if candidate not in removals
    )
    if candidates_new == cell.candidates:
        return cell
    return cell.model_copy(update={"candidates": candidates_new})
