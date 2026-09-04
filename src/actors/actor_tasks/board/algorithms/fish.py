from itertools import combinations
from shared.models.messages import Board, Cell


class Fish:
    @staticmethod
    def _candidate_rows(board: Board, candidate: int) -> dict[int, set[int]]:
        return {
            row: {
                cell.column
                for cell in board.cells
                if cell.row == row
                and cell.value is None
                and cell.candidates is not None
                and candidate in cell.candidates
            }
            for row in range(1, 10)
        }

    @staticmethod
    def _candidate_columns(board: Board, candidate: int) -> dict[int, set[int]]:
        return {
            column: {
                cell.row
                for cell in board.cells
                if cell.column == column
                and cell.value is None
                and cell.candidates is not None
                and candidate in cell.candidates
            }
            for column in range(1, 10)
        }

    @staticmethod
    def _remove_candidate(
        cell: Cell, candidate: int, affected: set[tuple[int, int]]
    ) -> Cell:
        if (
            (cell.row, cell.column) not in affected
            or cell.candidates is None
            or candidate not in cell.candidates
        ):
            return cell
        candidates = tuple(value for value in cell.candidates if value != candidate)
        if candidates == cell.candidates:
            return cell
        return cell.model_copy(update={"candidates": candidates})

    def _fish_rows(self, board: Board, candidate: int, size: int) -> Board:
        rows = self._candidate_rows(board, candidate)
        for selected_rows in combinations(range(1, 10), size):
            columns = set().union(*(rows[row] for row in selected_rows))
            if len(columns) != size:
                continue
            if any(
                not rows[row] or not rows[row].issubset(columns)
                for row in selected_rows
            ):
                continue
            affected = {
                (cell.row, cell.column)
                for cell in board.cells
                if cell.row not in selected_rows
                and cell.column in columns
                and cell.value is None
            }
            cells = tuple(
                self._remove_candidate(cell, candidate, affected)
                for cell in board.cells
            )
            if cells != board.cells:
                return board.model_copy(update={"cells": cells})
        return board

    def _fish_columns(self, board: Board, candidate: int, size: int) -> Board:
        columns = self._candidate_columns(board, candidate)
        for selected_columns in combinations(range(1, 10), size):
            rows = set().union(*(columns[column] for column in selected_columns))
            if len(rows) != size:
                continue
            if any(
                not columns[column] or not columns[column].issubset(rows)
                for column in selected_columns
            ):
                continue
            affected = {
                (cell.row, cell.column)
                for cell in board.cells
                if cell.column not in selected_columns
                and cell.row in rows
                and cell.value is None
            }
            cells = tuple(
                self._remove_candidate(cell, candidate, affected)
                for cell in board.cells
            )
            if cells != board.cells:
                return board.model_copy(update={"cells": cells})
        return board

    def _fish(self, board: Board, size: int) -> Board:
        for candidate in range(1, 10):
            updated = self._fish_rows(board, candidate, size)
            if updated != board:
                return updated
            updated = self._fish_columns(board, candidate, size)
            if updated != board:
                return updated
        return board

    def x_wing(self, board: Board) -> Board:
        return self._fish(board, 2)

    def swordfish(self, board: Board) -> Board:
        return self._fish(board, 3)

    def jellyfish(self, board: Board) -> Board:
        return self._fish(board, 4)