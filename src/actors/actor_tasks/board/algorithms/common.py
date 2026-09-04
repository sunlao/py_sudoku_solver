from collections.abc import Mapping
from shared.models.constants import CellIds
from shared.models.board import (
    CandidateRemoval,
    CandidateRemovals,
)
from shared.models.messages import Board, Cell


def add_removal(
    removals: CandidateRemovals, cell_id: CellIds, candidate: int
) -> CandidateRemovals:
    current = next(
        (removal for removal in removals.removals if removal.id == cell_id),
        None,
    )
    if current is None:
        return CandidateRemovals(
            removals=(
                *removals.removals,
                CandidateRemoval(
                    id=cell_id,
                    candidates=(candidate,),
                ),
            )
        )
    if candidate in current.candidates:
        return removals
    updated = current.model_copy(
        update={"candidates": (*current.candidates, candidate)}
    )
    return CandidateRemovals(
        removals=tuple(
            updated if removal.id == cell_id else removal
            for removal in removals.removals
        )
    )


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


def remove(board: Board, removals: CandidateRemovals) -> Board:
    cells = tuple(
        _remove_from_cell(
            cell,
            next(
                (
                    removal.candidates
                    for removal in removals.removals
                    if removal.id == cell.id
                ),
                (),
            ),
        )
        for cell in board.cells
    )
    if cells == board.cells:
        return board
    return board.model_copy(update={"cells": cells})


def _remove_from_cell(cell: Cell, removals: tuple[int, ...]) -> Cell:
    if cell.candidates is None or not removals:
        return cell
    candidates_new = tuple(
        candidate
        for candidate in cell.candidates
        if candidate not in removals
    )
    if candidates_new == cell.candidates:
        return cell
    return cell.model_copy(update={"candidates": candidates_new})
