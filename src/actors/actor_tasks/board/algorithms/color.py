from actors.actor_tasks.board.algorithms.common import (
    add_removal,
    candidates,
    remove,
    sees,
)
from shared.models.board import CandidateRemovals
from itertools import combinations
from actors.actor_tasks.board.algorithms.common import candidates, remove, sees
from shared.models.board import (
    ColoredCell,
    ColorComponent,
    ColorComponents,
    LinkedCellIds,
    StrongLink,
    StrongLinks,
)
from shared.models.constants import CellIds
from shared.models.messages import Board, Cell


class Color:

    @staticmethod
    def _cell(board: Board, cell_id: CellIds) -> Cell:
        return next(cell for cell in board.cells if cell.id == cell_id)

    def _color_component(self, links: StrongLinks, start: CellIds) -> ColorComponent:
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

    def _color_components(self, board: Board, candidate: int) -> ColorComponents:
        links = self._strong_links(board, candidate)
        components: tuple[ColorComponent, ...] = ()
        for link in links.links:
            if any(
                colored.id == link.left
                for component in components
                for colored in component.cells
            ):
                continue
            components = (
                *components,
                self._color_component(links, link.left),
            )
        return ColorComponents(components=components)

    @staticmethod
    def _linked_ids(
        links: StrongLinks,
        cell_id: CellIds,
    ) -> LinkedCellIds:
        linked_ids = tuple(
            link.right if link.left == cell_id else link.left
            for link in links.links
            if link.left == cell_id or link.right == cell_id
        )
        return LinkedCellIds(
            ids=tuple(
                linked_id
                for index, linked_id in enumerate(linked_ids)
                if linked_id not in linked_ids[:index]
            )
        )

    def _multi_coloring(
        self, board: Board, candidate: int, components: ColorComponents
    ) -> Board:
        removals = add_removal(removals, cell.id, candidate)
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
            valid_a = tuple(
                color
                for color in (0, 1)
                if any(truth_a == color for truth_a, _ in valid)
            )
            valid_b = tuple(
                color
                for color in (0, 1)
                if any(truth_b == color for _, truth_b in valid)
            )
            if len(valid_a) == 1:
                for colored in component_a.cells:
                    if colored.color != valid_a[0]:
                        removals[colored.id].add(candidate)
            if len(valid_b) == 1:
                for colored in component_b.cells:
                    if colored.color != valid_b[0]:
                        removals[colored.id].add(candidate)
        return remove(board, removals)

    def _simple_coloring(
        self, board: Board, candidate: int, components: ColorComponents
    ) -> Board:
        removals = add_removal(removals, cell.id, candidate)
        for component in components.components:
            component_ids = tuple(colored.id for colored in component.cells)
            for color in (0, 1):
                colored_cells = tuple(
                    self._cell(board, colored.id)
                    for colored in component.cells
                    if colored.color == color
                )
                if any(
                    sees(left, right) for left, right in combinations(colored_cells, 2)
                ):
                    for cell in colored_cells:
                        removals[cell.id].add(candidate)
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
            for cell in board.cells:
                if cell.id in component_ids or candidate not in candidates(cell):
                    continue
                if any(sees(cell, colored) for colored in color_a) and any(
                    sees(cell, colored) for colored in color_b
                ):
                    removals[cell.id].add(candidate)
        return remove(board, removals)

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
        links = tuple(
            StrongLink(left=cells[0].id, right=cells[1].id)
            for unit in units
            if len(
                cells := tuple(cell for cell in unit if candidate in candidates(cell))
            )
            == 2
        )
        return StrongLinks(links=links)

    def coloring(self, board: Board, multi: bool) -> Board:
        for candidate in range(1, 10):
            components = self._color_components(board, candidate)
            if not components.components:
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
