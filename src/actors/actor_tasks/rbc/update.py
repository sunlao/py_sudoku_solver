from datetime import datetime
from actors.actor_tasks.rbc.helpers.evaluate import Evaluate
from actors.actor_tasks.send import Send
from shared.models.constants import ActorDomainStatus
from shared.models.messages import Message, Cell, RBCCells, Metadata
from shared.models.side_effects import ActorSideEffects, PostControllerUpdate


class Update:

    def __init__(self):
        self.send = Send()
        self.evaluate = Evaluate()

    async def _send_controller(
        self,
        side_effects: ActorSideEffects,
        dto: Message,
        director_now: datetime,
        sending_status: ActorDomainStatus,
    ) -> None:
        """Send controntrol:update message the rbc actor status"""
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        send_dto = PostControllerUpdate(
            side_effects=side_effects,
            sending_actor=actor,
            sending_status=sending_status,
            last_director_timestamp=director_now,
            rbc_flag=True,
        )
        await self.send.post_controller_update(send_dto)

    async def _send_game(
        self, side_effects: ActorSideEffects, cells: tuple[Cell, ...]
    ) -> None:
        """Send game:update message for each updated cell"""
        await side_effects.gather(
            *(self.send.post_game_update(side_effects, c) for c in cells)
        )

    async def _send_rbc(
        self,
        side_effects: ActorSideEffects,
        dto: Message,
        cells: tuple[Cell, ...],
    ) -> None:
        """Send rbc:update message for each effected behavior maped to cell"""
        static_data = side_effects.static_data(dto).rbc_cell_behavior_maps()
        messages = tuple(
            Message[Cell](
                metadata=Metadata(actor_behavior=behavior, rbc_flag=True),
                content=cell,
            )
            for cell in cells
            for map in static_data.maps
            if map.id == cell.id
            for behavior in map.behaviors
        )
        await side_effects.gather(
            *(self.send.post_rbc_update(side_effects, m) for m in messages)
        )

    @staticmethod
    def _updated_cells(old: RBCCells, new: RBCCells) -> tuple[Cell, ...]:
        return tuple(
            new_cell
            for old_cell, new_cell in zip(old.cells, new.cells, strict=True)
            if old_cell != new_cell
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[Cell]
    ) -> None:
        director_now = side_effects.now()
        rbc_old = side_effects.state.get_cache(dto)
        cell = dto.content
        old_cell = next(c for c in rbc_old.cells if c.id == cell.id)
        if old_cell.value is not None:
            await self._send_controller(
                side_effects, dto, director_now, ActorDomainStatus.DONE
            )
            print("**rbc:update NoOp")
            return None
        rbc_update = rbc_old.model_copy(
            update={
                "cells": tuple(
                    cell if c.id == cell.id else c
                    for c in rbc_old.cells
                )
            }
        )
        rbc_new = await self.evaluate.all(side_effects, rbc_update)
        updated_cells = self._updated_cells(rbc_old, rbc_new)
        await side_effects.gather(
            self._send_game(side_effects, updated_cells),
            self._send_rbc(side_effects, dto, updated_cells),
            self._send_controller(
                side_effects, dto, director_now, ActorDomainStatus.WORKING
            ),
        )
        side_effects.state.set_rbc_cells(dto, rbc_new)
        print("**rbc:update end")
