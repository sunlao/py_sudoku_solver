from itertools import combinations
from actors.actor_tasks.board.algorithms.common import sees
from shared.models.board import (
    ColoredCell,
    ColorComponent,
    ColorComponents,
    StrongLink,
    StrongLinks,
)
from shared.models.constants import CellIds
from shared.models.messages import Board, Cell


class Color:
    @staticmethod
    def _cell(board: Board, cell_id: CellIds) -> Cell:
        return next(cell for cell in board.cells if cell.id == cell_id)

    @staticmethod
    def _remove(cell: Cell, candidate: int, remove: bool) -> Cell:
        if not remove or cell.candidates is None or candidate not in cell.candidates:
            return cell
        candidates = tuple(value for value in cell.candidates if value != candidate)
        return cell.model_copy(update={"candidates": candidates})

    def _strong_links(self, board: Board, candidate: int) -> StrongLinks:
        units = (
            *(
                tuple(cell for cell in board.cells if cell.row == row)
                for row in range(1, 10)
            ),
            *(
                tuple(cell for cell in board.cells if cell.column == column)
                for column in range(1, 10)
            ),
            *(
                tuple(cell for cell in board.cells if cell.box == box)
                for box in range(1, 10)
            ),
        )
        links: tuple[StrongLink, ...] = ()
        for unit in units:
            cells = tuple(
                cell
                for cell in unit
                if cell.value is None
                and cell.candidates is not None
                and candidate in cell.candidates
            )
            if len(cells) != 2:
                continue
            link = StrongLink(left=cells[0].id, right=cells[1].id)
            duplicate = any(
                (current.left == link.left and current.right == link.right)
                or (current.left == link.right and current.right == link.left)
                for current in links
            )
            if not duplicate:
                links = (*links, link)
        return StrongLinks(links=links)

    def _color_component(self, links: StrongLinks, start: CellIds) -> ColorComponent:
        pending = (ColoredCell(id=start, color=0),)
        colored: tuple[ColoredCell, ...] = ()
        while pending:
            current = pending[0]
            pending = pending[1:]
            if any(cell.id == current.id for cell in colored):
                continue
            colored = (*colored, current)
            linked_color = 1 if current.color == 0 else 0
            linked_ids = tuple(
                link.right if link.left == current.id else link.left
                for link in links.links
                if link.left == current.id or link.right == current.id
            )
            additions = tuple(
                ColoredCell(id=linked_id, color=linked_color)
                for index, linked_id in enumerate(linked_ids)
                if linked_id not in linked_ids[:index]
                and not any(cell.id == linked_id for cell in colored)
                and not any(cell.id == linked_id for cell in pending)
            )
            pending = (*pending, *additions)
        return ColorComponent(cells=colored)

    def _color_components(self, board: Board, candidate: int) -> ColorComponents:
        links = self._strong_links(board, candidate)
        components: tuple[ColorComponent, ...] = ()
        for link in links.links:
            assigned = any(
                colored.id == link.left
                for component in components
                for colored in component.cells
            )
            if not assigned:
                components = (*components, self._color_component(links, link.left))
        return ColorComponents(components=components)

    def _simple_remove(
        self, board: Board, cell: Cell, candidate: int, components: ColorComponents
    ) -> bool:
        if cell.candidates is None or candidate not in cell.candidates:
            return False
        for component in components.components:
            assigned = next(
                (colored for colored in component.cells if colored.id == cell.id), None
            )
            if assigned is not None:
                same_color = tuple(
                    self._cell(board, colored.id)
                    for colored in component.cells
                    if colored.color == assigned.color
                )
                if any(
                    sees(left, right) for left, right in combinations(same_color, 2)
                ):
                    return True
                continue
            color_a = tuple(
                self._cell(board, colored.id)
                for colored in component.cells
                if colored.color == 0
            )
            color_b = tuple(
                self._cell(board, colored.id)
                for colored in component.cells
                if colored.color == 1
            )
            if any(sees(cell, colored) for colored in color_a) and any(
                sees(cell, colored) for colored in color_b
            ):
                return True
        return False

    def _simple_coloring(
        self, board: Board, candidate: int, components: ColorComponents
    ) -> Board:
        cells = tuple(
            self._remove(
                cell,
                candidate,
                self._simple_remove(board, cell, candidate, components),
            )
            for cell in board.cells
        )
        if cells == board.cells:
            return board
        return board.model_copy(update={"cells": cells})

    def _multi_remove(
        self, board: Board, cell: Cell, candidate: int, components: ColorComponents
    ) -> bool:
        if cell.candidates is None or candidate not in cell.candidates:
            return False
        for component_a, component_b in combinations(components.components, 2):
            valid = tuple(
                (truth_a, truth_b)
                for truth_a in (0, 1)
                for truth_b in (0, 1)
                if not any(
                    sees(left, right)
                    for left in (
                        self._cell(board, colored.id)
                        for colored in component_a.cells
                        if colored.color == truth_a
                    )
                    for right in (
                        self._cell(board, colored.id)
                        for colored in component_b.cells
                        if colored.color == truth_b
                    )
                )
            )
            if not valid:
                continue
            assigned_a = next(
                (colored for colored in component_a.cells if colored.id == cell.id),
                None,
            )
            assigned_b = next(
                (colored for colored in component_b.cells if colored.id == cell.id),
                None,
            )
            valid_a = tuple(
                color for color in (0, 1) if any(left == color for left, _ in valid)
            )
            valid_b = tuple(
                color for color in (0, 1) if any(right == color for _, right in valid)
            )
            if (
                assigned_a is not None
                and len(valid_a) == 1
                and assigned_a.color != valid_a[0]
            ):
                return True
            if (
                assigned_b is not None
                and len(valid_b) == 1
                and assigned_b.color != valid_b[0]
            ):
                return True
        return False

    def _multi_coloring(
        self, board: Board, candidate: int, components: ColorComponents
    ) -> Board:
        cells = tuple(
            self._remove(
                cell,
                candidate,
                self._multi_remove(board, cell, candidate, components),
            )
            for cell in board.cells
        )
        if cells == board.cells:
            return board
        return board.model_copy(update={"cells": cells})

    def simple(self, board: Board) -> Board:
        for candidate in range(1, 10):
            components = self._color_components(board, candidate)
            if components.components:
                updated = self._simple_coloring(board, candidate, components)
                if updated != board:
                    return updated
        return board

    def multi(self, board: Board) -> Board:
        for candidate in range(1, 10):
            components = self._color_components(board, candidate)
            if components.components:
                updated = self._multi_coloring(board, candidate, components)
                if updated != board:
                    return updated
        return board