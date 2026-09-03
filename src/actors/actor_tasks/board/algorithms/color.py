from collections import defaultdict, deque
from itertools import combinations
from actors.actor_tasks.board.algorithms.common import (
    candidates,
    cell_map,
    remove,
    sees,
)
from shared.models.constants import CellIds
from shared.models.messages import Board
from shared.models.board import (
    ColoredCell,
    ColorComponent,
    ColorComponents,
    StrongLink,
    StrongLinks,
)


class Color:

    def _strong_links(self, board: Board, candidate: int) -> StrongLinks:
        units = (
            *(tuple(cell for cell in board.cells if cell.row == row) for row in range(1, 10)),
            *(
                tuple(cell for cell in board.cells if cell.column == column)
                for column in range(1, 10)
            ),
            *(tuple(cell for cell in board.cells if cell.box == box) for box in range(1, 10)),
        )
        links = tuple(
            StrongLink(left=cells[0].id, right=cells[1].id)
            for unit in units
            if len(
                cells := tuple(
                    cell for cell in unit if candidate in candidates(cell)
                )
            )
            == 2
        )
        return StrongLinks(links=links)

    def _color_component(
        self,
        links: StrongLinks,
        start: CellIds,
    ) -> ColorComponent:
        pending = (ColoredCell(id=start, color=0),)
        colored: tuple[ColoredCell, ...] = ()
        while pending:
            current = pending[0]
            pending = pending[1:]
            if any(cell.id == current.id for cell in colored):
                continue
            colored = (*colored, current)
            linked_color = 1 - current.color
            additions = tuple(
                ColoredCell(id=linked_id, color=linked_color)
                for linked_id in self._linked_ids(links, current.id)
                if not any(cell.id == linked_id for cell in colored)
                and not any(cell.id == linked_id for cell in pending)
            )
            pending = (*pending, *additions)
        return ColorComponent(cells=colored)

    def _simple_coloring(
        self, board: Board, candidate: int, components: list[dict[CellIds, int]]
    ) -> Board:
        cells = cell_map(board)
        removals: dict[CellIds, set[int]] = defaultdict(set)
        for component in components:
            for color in (0, 1):
                colored = tuple(
                    cells[cell_id]
                    for cell_id, value in component.items()
                    if value == color
                )
                if any(sees(a, b) for a, b in combinations(colored, 2)):
                    for cell in colored:
                        removals[cell.id].add(candidate)
            color_a = tuple(
                cells[cell_id] for cell_id, color in component.items() if color == 0
            )
            color_b = tuple(
                cells[cell_id] for cell_id, color in component.items() if color == 1
            )
            for cell in board.cells:
                if cell.id in component or candidate not in candidates(cell):
                    continue
                if any(sees(cell, c) for c in color_a) and any(
                    sees(cell, c) for c in color_b
                ):
                    removals[cell.id].add(candidate)
        return remove(board, removals)

    def _multi_coloring(
        self, board: Board, candidate: int, components: list[dict[CellIds, int]]
    ) -> Board:
        cells = cell_map(board)
        removals: dict[CellIds, set[int]] = defaultdict(set)
        for component_a, component_b in combinations(components, 2):
            valid: set[tuple[int, int]] = set()
            for truth_a in (0, 1):
                for truth_b in (0, 1):
                    true_a = tuple(
                        cells[cell_id]
                        for cell_id, color in component_a.items()
                        if color == truth_a
                    )
                    true_b = tuple(
                        cells[cell_id]
                        for cell_id, color in component_b.items()
                        if color == truth_b
                    )
                    conflict = any(sees(a, b) for a in true_a for b in true_b)
                    if not conflict:
                        valid.add((truth_a, truth_b))
            if not valid:
                continue
            valid_a = {a for a, _ in valid}
            valid_b = {b for _, b in valid}
            if len(valid_a) == 1:
                true_color = next(iter(valid_a))
                for cell_id, color in component_a.items():
                    if color != true_color:
                        removals[cell_id].add(candidate)
            if len(valid_b) == 1:
                true_color = next(iter(valid_b))
                for cell_id, color in component_b.items():
                    if color != true_color:
                        removals[cell_id].add(candidate)
        return remove(board, removals)

    def coloring(self, board: Board, multi: bool) -> Board:
        for candidate in range(1, 10):
            components = self._color_components(board, candidate)
            if not components:
                continue
            updated = self._simple_coloring(
                board,
                candidate,
                components,
            )
            if updated != board:
                return updated
            if multi:
                updated = self._multi_coloring(
                    board,
                    candidate,
                    components,
                )
                if updated != board:
                    return updated
        return board
