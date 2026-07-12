from shared.models.constants import CellIds
from shared.models.messages import RBCCells


class Notify:

    def _updated_cell_ids(self, old: RBCCells, new: RBCCells) -> tuple[CellIds, ...]:
        return tuple(
            new_cell.id
            for old_cell, new_cell in zip(old.cells, new.cells, strict=True)
            if old_cell.value != new_cell.value
            or old_cell.candidates != new_cell.candidates
        )