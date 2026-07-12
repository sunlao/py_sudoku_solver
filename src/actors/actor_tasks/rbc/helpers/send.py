from shared.models.board import CellBehaviorMaps, CellBehaviors
from shared.models.constants import CellIds
from shared.models.messages import Message, RBCCells, Cell, Metadata, ActorBehaviors
from shared.models.side_effects import ActorSideEffects


class Send:

    def _message(self, actor_behaviors: ActorBehaviors, cell: Cell) -> Message[Cell]:
        actor, _ = actor_behaviors.split(".", maxsplit=1)
        m = Metadata(actor_behavior=ActorBehaviors(f"{actor}.update"), rbc_flag=True)
        return Message(metadata=m, content=cell)

    def _messages(
        self, maps: CellBehaviorMaps, rbc: RBCCells
    ) -> tuple[Message[Cell], ...]:
        return tuple(
            self._message(actor_behavior, cell)
            for cell_behaviors in maps.maps
            for cell in rbc.cells
            if cell.id == cell_behaviors.id
            for actor_behavior in cell_behaviors.behaviors
        )

    @staticmethod
    def _cell_behaviors(id: CellIds, maps: CellBehaviorMaps) -> CellBehaviors:
        return next((m for m in maps.maps if m.id == id))

    def _cell_behavior_maps(
        self,
        cell_ids: frozenset[CellIds],
        maps: CellBehaviorMaps,
    ) -> CellBehaviorMaps:
        return CellBehaviorMaps(
            maps=tuple(self._cell_behaviors(i, maps) for i in cell_ids)
        )

    def _updated_cell_ids(self, old: RBCCells, new: RBCCells) -> frozenset[CellIds]:
        return frozenset(
            new_cell.id
            for old_cell, new_cell in zip(old.cells, new.cells, strict=True)
            if old_cell.value != new_cell.value
            or old_cell.candidates != new_cell.candidates
        )

    async def rbcs(
        self, side_effects: ActorSideEffects, dto: Message[RBCCells], new: RBCCells
    ):
        ids = self._updated_cell_ids(dto.content, new)
        maps = side_effects.static_data(dto).rbc_cell_behavior_maps()
        cell_behavior_maps = self._cell_behavior_maps(ids, maps)
        messages = self._messages(cell_behavior_maps, new)
        await side_effects.gather(
            *(side_effects.mailbox.enqueue(message) for message in messages)
        )