from actors.actor_tasks.board.algorithms.intersection import Board
from actors.actor_tasks.board.algorithms.color import Color
from actors.actor_tasks.board.algorithms.fish import Fish
from actors.actor_tasks.board.algorithms.xy import XY
from shared.models.messages import Board, Cell
from shared.models.side_effects import ActorSideEffects


class Evaluate:

    def __init__(self) -> None:
        self.board = Board()
        self.color = Color()
        self.fish = Fish()
        self.xy = XY()

    @staticmethod
    def _merge_cells(results: tuple[Cell, ...]) -> Cell:
        cell = results[0]
        candidates_set = [
            set(result.candidates)
            for result in results
            if result.candidates is not None
        ]
        candidates = (
            tuple(sorted(set.intersection(*candidates_set))) if candidates_set else None
        )
        if cell.candidates == candidates:
            return cell
        return cell.model_copy(update={"candidates": candidates})

    def _merge_boards(self, results: list[Board]) -> Board:
        board = results[0]
        cells = tuple(
            self._merge_cells(cells)
            for cells in zip(*(result.cells for result in results), strict=True)
        )
        if board.cells == cells:
            return board
        return board.model_copy(update={"cells": cells})

    async def all(self, side_effects: ActorSideEffects, board: Board) -> Board:
        results = await side_effects.gather(
            side_effects.run_sync(self.fish.fish, board, 2),
            side_effects.run_sync(self.fish.fish, board, 3),
            side_effects.run_sync(self.fish.fish, board, 4),
            side_effects.run_sync(self.xy.y_wing, board),
            side_effects.run_sync(self.xy.xyz_wing, board),
            side_effects.run_sync(self.color.coloring, board, False),
            side_effects.run_sync(self.color.coloring, board, True),
            side_effects.run_sync(self.xy.xy_chain, board),
            side_effects.run_sync(self.board.forcing_chains, board),
            side_effects.run_sync(self.board.unique_rectangle, board),
            side_effects.run_sync(self.board.pointing, board),
            side_effects.run_sync(self.board.box_line, board),
        )
        return self._merge_boards(results)
