from datetime import datetime
from actors.actor_tasks.send import Send
from shared.models.constants import ActorDomainStatus
from shared.models.messages import Board, Cell, Message
from shared.models.side_effects import ActorSideEffects, PostControllerUpdate


class Update:

    def __init__(self) -> None:
        self.send = Send()

    @staticmethod
    def _new_board(board: Board, cell: Cell) -> Board:
        return board.model_copy(
            update={
                "cells": tuple(
                    cell if c.id == cell.id else c
                    for c in board.cells
                )
            }
        )

    @staticmethod
    def _status(board: Board) -> ActorDomainStatus:
        return (
            ActorDomainStatus.WORKING
            if any(cell.value is None for cell in board.cells)
            else ActorDomainStatus.DONE
        )

    async def _send_controller(
        self,
        side_effects: ActorSideEffects,
        dto: Message[Cell],
        director_now: datetime,
        sending_status: ActorDomainStatus,
    ) -> None:
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        send_dto = PostControllerUpdate(
            side_effects=side_effects,
            sending_actor=actor,
            sending_status=sending_status,
            last_director_timestamp=director_now,
            rbc_flag=False,
        )
        await self.send.post_controller_update(send_dto)

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[Cell]
    ) -> None:
        director_now = side_effects.now()
        board: Board = side_effects.state.get_cache(dto)
        cell = dto.content
        old_cell = next(c for c in board.cells if c.id == cell.id)

        if old_cell.value is not None:
            await self._send_controller(
                side_effects, dto, director_now, self._status(board)
            )
            print("**game:update NoOp")
            return None

        board_new = self._new_board(board, cell)
        side_effects.state.set_game_board(dto, board_new)
        await self._send_controller(
            side_effects, dto, director_now, self._status(board_new)
        )
        print("**game:update end")