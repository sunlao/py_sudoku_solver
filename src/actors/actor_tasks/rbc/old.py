from fastapi import status
from shared.models.board import CellBehaviorMaps, CellBehaviors
from shared.models.constants import ActorBehaviors, ActorNames, CellIds
from shared.models.messages import Cell, Message, Metadata, RBCCells
from shared.models.side_effects import ActorSideEffects


class Solve:
    @staticmethod
    async def _post_msg(side_effects: ActorSideEffects, dto: Message) -> None:
        async with side_effects.transport_client(
            side_effects.fastapi_app, dto
        ) as client:
            response = await client.post("/", json=dto.model_dump(mode="json"))
            if response.status_code != status.HTTP_202_ACCEPTED:
                raise RuntimeError(
                    f"{dto.metadata.actor_behavior} failed to send "
                    f"MessageID: {dto.metadata.message_id}"
                )

    @staticmethod
    def _updated_cells(old: RBCCells, new: RBCCells) -> tuple[Cell, ...]:
        return tuple(
            new_cell
            for old_cell, new_cell in zip(old.cells, new.cells, strict=True)
            if old_cell != new_cell
        )

    @staticmethod
    def _cell_behaviors(id: CellIds, maps: CellBehaviorMaps) -> CellBehaviors:
        return next(m for m in maps.maps if m.id == id)

    async def send_game_update(
        self, side_effects: ActorSideEffects, old: RBCCells, new: RBCCells
    ) -> None:
        messages = tuple(
            Message[Cell](
                metadata=Metadata(actor_behavior=ActorBehaviors.GAME_CELL_UPDATE),
                content=cell,
            )
            for cell in self._updated_cells(old, new)
        )
        await side_effects.gather(
            *(self._post_msg(side_effects, message) for message in messages)
        )

    async def send_rbc_evaluate(
        self,
        side_effects: ActorSideEffects,
        dto: Message,
        old: RBCCells,
        new: RBCCells,
    ) -> None:
        updated_cells = self._updated_cells(old, new)
        maps = side_effects.static_data(dto).rbc_cell_behavior_maps()
        actors = frozenset(
            ActorNames(actor_behavior.split(".", maxsplit=1)[0])
            for cell in updated_cells
            for actor_behavior in self._cell_behaviors(cell.id, maps).behaviors
        )
        messages = tuple(
            Message[RBCCells](
                metadata=Metadata(
                    actor_behavior=ActorBehaviors(f"{actor}.evaluate"),
                    rbc_flag=True,
                ),
                content=RBCCells(actor=actor, cells=...),
            )
            for actor in actors
        )
        await side_effects.gather(
            *(self._post_msg(side_effects, message) for message in messages)
        )
        print("**rbd: evaluate end ")
