from shared.models.messages import ActorNames, Cell, CellIds, RBCCells


def candidates(cells: RBCCells, cell_id: CellIds) -> Cell:
    return next(sorted(c.candidates) for c in cells.cells if c.id == cell_id)


def value(cells: RBCCells, cell_id: CellIds) -> Cell:
    return next(c.value for c in cells.cells if c.id == cell_id)


def cell(cells: RBCCells, cell_id: CellIds) -> Cell:
    return next(c for c in cells.cells if c.id == cell_id)


def rbc_cells(*cells: Cell) -> RBCCells:
    return RBCCells(actor=ActorNames.ROW1, cells=cells)
