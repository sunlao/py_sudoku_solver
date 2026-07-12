from shared.models.constants import CellIds
from shared.models.messages import Message, RBCCells
from shared.models.side_effects import ActorSideEffects



class Send:

    def _updated_cell_ids(self, old: RBCCells, new: RBCCells) -> tuple[CellIds, ...]:
        return tuple(
            new_cell.id
            for old_cell, new_cell in zip(old.cells, new.cells, strict=True)
            if old_cell.value != new_cell.value
            or old_cell.candidates != new_cell.candidates
        )

    def rbcs(self, side_effects: ActorSideEffects, dto: Message[RBCCells], new: RBCCells):
        maps = side_effects.static_data(dto).rbc_cell_behavior_maps()
        updated_cell_ids = self._updated_cell_ids(dto.content, new)
