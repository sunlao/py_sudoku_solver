from actors.actor_tasks.board.algorithms.fish import Fish
from shared.models.messages import Board, Cell
from shared.models.side_effects import ActorSideEffects


class Evaluate:

    def __init__(self) -> None:
        self.algorithms = Fish()

    @staticmethod
    def _merge_cells(results: tuple[Cell, ...]) -> Cell:
        cell = results[0]
        candidates_set = [
            set(c.candidates) for c in results if c.candidates is not None
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
            for cells in zip(*(r.cells for r in results), strict=True)
        )
        if board.cells == cells:
            return board
        return board.model_copy(update={"cells": cells})

    async def all(self, side_effects: ActorSideEffects, board: Board) -> Board:
        results = await side_effects.gather(
            side_effects.run_sync(self.algorithms.fish, board, 2),
            side_effects.run_sync(self.algorithms.fish, board, 3),
            side_effects.run_sync(self.algorithms.fish, board, 4),
            side_effects.run_sync(self.algorithms.y_wing, board),
            side_effects.run_sync(self.algorithms.xyz_wing, board),
            side_effects.run_sync(self.algorithms.coloring, board, False),
            side_effects.run_sync(self.algorithms.coloring, board, True),
            side_effects.run_sync(self.algorithms.xy_chain, board),
            side_effects.run_sync(self.algorithms.forcing_chains, board),
            side_effects.run_sync(self.algorithms.unique_rectangle, board),
            side_effects.run_sync(self.algorithms.pointing, board),
            side_effects.run_sync(self.algorithms.box_line, board),
        )
        return self._merge_boards(results)
