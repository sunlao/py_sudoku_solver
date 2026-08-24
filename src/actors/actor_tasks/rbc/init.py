from datetime import datetime
from actors.actor_tasks.rbc.helpers.evaluate import Evaluate
from actors.actor_tasks.send import Send
from shared.models.constants import ActorDomainStatus
from shared.models.messages import  Message, Cell, RBCCells
from shared.models.side_effects import ActorSideEffects, PostControllerUpdate

class Init:

    def __init__(self):
        self.send = Send()
        self.evaluate = Evaluate()

    async def _send_controller(
            self,
            side_effects: ActorSideEffects,
            dto: Message[RBCCells],
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
            rbc_flag=True
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
            self, side_effects: ActorSideEffects, cells: tuple[Cell, ...]
        ) -> None:
        """Send rbc:evaluate message for each updated cell"""
        await side_effects.gather(
            *(self.send.post_rbc_update(side_effects, c) for c in cells)
        )

    @staticmethod
    def _updated_cells(old: RBCCells, new: RBCCells) -> tuple[Cell, ...]:
        return tuple(
            new_cell
            for old_cell, new_cell in zip(old.cells, new.cells, strict=True)
            if old_cell != new_cell
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[RBCCells]
    ) -> None:
        director_now = side_effects.now()
        rbc_old = dto.content
        rbc_new = await self.evaluate.all(side_effects, dto.content)
        updated_cells = self._updated_cells(rbc_old, rbc_new)
        await self._send_game(side_effects, updated_cells)
        await self._send_controller(
            side_effects, dto, director_now, ActorDomainStatus.DONE
        )
        side_effects.state.set_rbc_cells(dto, rbc_new)
        print("**rbc:eval end")

