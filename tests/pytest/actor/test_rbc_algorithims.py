from shared.models.messages import ActorNames, Cell, CellIds, RBCCells


def cell(cells: RBCCells, cell_id: CellIds) -> Cell:
    return next(c for c in cells.cells if c.id == cell_id)


def rbc_cells(*cells: Cell) -> RBCCells:
    return RBCCells(actor=ActorNames.ROW1, cells=cells)


def test_hidden_1(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=5),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=6),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=7),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=8),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None),
    )
    result = rbc_algorithms.hidden(cells, 1)
    assert cell(result, CellIds.R1C9).value == 9
    assert cell(result, CellIds.R1C9).candidates == (9,)


def test_hidden_2(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(5, 6, 7)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(5, 6, 8)),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(7, 8, 9)),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(7, 8, 9)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(7, 8, 9)),
    )
    result = rbc_algorithms.hidden(cells, 2)
    assert cell(result, CellIds.R1C5).candidates == (5, 6)
    assert cell(result, CellIds.R1C6).candidates == (5, 6)
    assert cell(result, CellIds.R1C7).candidates == (7, 8, 9)
    assert cell(result, CellIds.R1C8).candidates == (7, 8, 9)
    assert cell(result, CellIds.R1C9).candidates == (7, 8, 9)


def test_hidden_3(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=None, candidates=(3, 4, 5, 6)),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=None, candidates=(3, 4, 5, 7)),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(3, 4, 5, 8)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(6, 7, 8, 9)),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(6, 7, 8, 9)),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(6, 7, 8, 9)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(6, 7, 8, 9)),
    )
    result = rbc_algorithms.hidden(cells, 3)
    assert cell(result, CellIds.R1C3).candidates == (3, 4, 5)
    assert cell(result, CellIds.R1C4).candidates == (3, 4, 5)
    assert cell(result, CellIds.R1C5).candidates == (3, 4, 5)
    assert cell(result, CellIds.R1C6).candidates == (6, 7, 8, 9)
    assert cell(result, CellIds.R1C7).candidates == (6, 7, 8, 9)
    assert cell(result, CellIds.R1C8).candidates == (6, 7, 8, 9)
    assert cell(result, CellIds.R1C9).candidates == (6, 7, 8, 9)


def test_naked_1(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=5),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=6),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=7),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=8),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None),
    )
    result = rbc_algorithms.naked(cells, 1)
    assert cell(result, CellIds.R1C9).value == 9
    assert cell(result, CellIds.R1C9).candidates == (9,)


def test_naked_2(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(5, 6)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(5, 6)),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(5, 6, 7)),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(5, 6, 8)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(7, 8, 9)),
    )
    result = rbc_algorithms.naked(cells, 2)
    assert cell(result, CellIds.R1C5).candidates == (5, 6)
    assert cell(result, CellIds.R1C6).candidates == (5, 6)
    assert cell(result, CellIds.R1C7).value == 7
    assert cell(result, CellIds.R1C7).candidates == (7,)
    assert cell(result, CellIds.R1C8).value == 8
    assert cell(result, CellIds.R1C8).candidates == (8,)
    assert cell(result, CellIds.R1C9).candidates == (7, 8, 9)


def test_naked_3(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=None, candidates=(3, 4, 5)),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=None, candidates=(3, 4, 5)),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(3, 4, 5)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(3, 4, 5, 6)),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(3, 4, 5, 7)),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(3, 4, 5, 8)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(6, 7, 8, 9)),
    )
    result = rbc_algorithms.naked(cells, 3)
    assert cell(result, CellIds.R1C3).candidates == (3, 4, 5)
    assert cell(result, CellIds.R1C4).candidates == (3, 4, 5)
    assert cell(result, CellIds.R1C5).candidates == (3, 4, 5)
    assert cell(result, CellIds.R1C6).value == 6
    assert cell(result, CellIds.R1C6).candidates == (6,)
    assert cell(result, CellIds.R1C7).value == 7
    assert cell(result, CellIds.R1C7).candidates == (7,)
    assert cell(result, CellIds.R1C8).value == 8
    assert cell(result, CellIds.R1C8).candidates == (8,)
    assert cell(result, CellIds.R1C9).candidates == (6, 7, 8, 9)
