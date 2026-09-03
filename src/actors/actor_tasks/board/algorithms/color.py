from collections import defaultdict, deque
from itertools import combinations

from shared.models.constants import CellIds
from shared.models.messages import Board


class Color:

    def _strong_links(
        self, board: Board, candidate: int
    ) -> dict[CellIds, set[CellIds]]:
        links: dict[CellIds, set[CellIds]] = defaultdict(set)
        units = []
        for row in range(1, 10):
            units.append(tuple(c for c in board.cells if c.row == row))
        for column in range(1, 10):
            units.append(tuple(c for c in board.cells if c.column == column))
        for box in range(1, 10):
            units.append(tuple(c for c in board.cells if c.box == box))
        for unit in units:
            cells = tuple(cell for cell in unit if candidate in self._candidates(cell))
            if len(cells) != 2:
                continue
            a, b = cells
            links[a.id].add(b.id)
            links[b.id].add(a.id)
        return links

    def _color_components(
        self, board: Board, candidate: int
    ) -> list[dict[CellIds, int]]:
        links = self._strong_links(board, candidate)
        components: list[dict[CellIds, int]] = []
        visited: set[CellIds] = set()
        for start in links:
            if start in visited:
                continue
            colors: dict[CellIds, int] = {start: 0}
            queue = deque([start])
            while queue:
                current = queue.popleft()
                visited.add(current)
                for linked in links[current]:
                    expected = 1 - colors[current]
                    if linked not in colors:
                        colors[linked] = expected
                        queue.append(linked)
            components.append(colors)
        return components

    def _simple_coloring(
        self,
        board: Board,
        candidate: int,
        components: list[dict[CellIds, int]],
    ) -> Board:
        cells = self._cell_map(board)
        removals: dict[CellIds, set[int]] = defaultdict(set)
        for component in components:
            for color in (0, 1):
                colored = tuple(
                    cells[cell_id]
                    for cell_id, value in component.items()
                    if value == color
                )
                if any(self._sees(a, b) for a, b in combinations(colored, 2)):
                    for cell in colored:
                        removals[cell.id].add(candidate)
            color_a = tuple(
                cells[cell_id] for cell_id, color in component.items() if color == 0
            )
            color_b = tuple(
                cells[cell_id] for cell_id, color in component.items() if color == 1
            )
            for cell in board.cells:
                if cell.id in component or candidate not in self._candidates(cell):
                    continue
                if any(self._sees(cell, c) for c in color_a) and any(
                    self._sees(cell, c) for c in color_b
                ):
                    removals[cell.id].add(candidate)
        return self._remove(board, removals)

    def _multi_coloring(
        self,
        board: Board,
        candidate: int,
        components: list[dict[CellIds, int]],
    ) -> Board:
        cells = self._cell_map(board)
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
                    conflict = any(self._sees(a, b) for a in true_a for b in true_b)
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
        return self._remove(board, removals)

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
