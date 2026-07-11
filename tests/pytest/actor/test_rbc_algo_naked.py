from helpers.algorithms import candidates, rbc_cells, value
from shared.models.messages import Cell, CellIds


def test_size_1(rbc_algorithms):
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
    assert value(result, CellIds.R1C9) == 9
    assert candidates(result, CellIds.R1C9) == [9]


def test_size_2(rbc_algorithms):
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
    assert candidates(result, CellIds.R1C5) == [5, 6]
    assert candidates(result, CellIds.R1C6) == [5, 6]
    assert value(result, CellIds.R1C7) == 7
    assert candidates(result, CellIds.R1C7) == [7]
    assert value(result, CellIds.R1C8) == 8
    assert candidates(result, CellIds.R1C8) == [8]
    assert candidates(result, CellIds.R1C9) == [7, 8, 9]


def test_size_3(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=None, candidates=(3, 4, 5)),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=None, candidates=(3, 4, 5)),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(3, 4, 5)),
        Cell(
            id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(3, 4, 5, 6)
        ),
        Cell(
            id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(3, 4, 5, 7)
        ),
        Cell(
            id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(3, 4, 5, 8)
        ),
        Cell(
            id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(6, 7, 8, 9)
        ),
    )
    result = rbc_algorithms.naked(cells, 3)
    assert candidates(result, CellIds.R1C3) == [3, 4, 5]
    assert candidates(result, CellIds.R1C4) == [3, 4, 5]
    assert candidates(result, CellIds.R1C5) == [3, 4, 5]
    assert value(result, CellIds.R1C6) == 6
    assert candidates(result, CellIds.R1C6) == [6]
    assert value(result, CellIds.R1C7) == 7
    assert candidates(result, CellIds.R1C7) == [7]
    assert value(result, CellIds.R1C8) == 8
    assert candidates(result, CellIds.R1C8) == [8]
    assert candidates(result, CellIds.R1C9) == [6, 7, 8, 9]


def test_no_naked_found(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(5, 6, 7)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(5, 6, 8)),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(5, 7, 9)),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(6, 8, 9)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(7, 8, 9)),
    )
    result = rbc_algorithms.naked(cells, 2)
    assert candidates(result, CellIds.R1C5) == [5, 6, 7]
    assert candidates(result, CellIds.R1C6) == [5, 6, 8]
    assert candidates(result, CellIds.R1C7) == [5, 7, 9]
    assert candidates(result, CellIds.R1C8) == [6, 8, 9]
    assert candidates(result, CellIds.R1C9) == [7, 8, 9]


def test_not_needed_no_naked(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(5, 6)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(5, 6)),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(7, 8, 9)),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(7, 8, 9)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(7, 8, 9)),
    )
    result = rbc_algorithms.naked(cells, 2)
    assert candidates(result, CellIds.R1C5) == [5, 6]
    assert candidates(result, CellIds.R1C6) == [5, 6]
    assert candidates(result, CellIds.R1C7) == [7, 8, 9]
    assert candidates(result, CellIds.R1C8) == [7, 8, 9]
    assert candidates(result, CellIds.R1C9) == [7, 8, 9]


def test_not_needed_too_many_candidates(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(5, 6)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(5, 7)),
        Cell(
            id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(5, 6, 7, 8)
        ),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(6, 8, 9)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(7, 8, 9)),
    )
    result = rbc_algorithms.naked(cells, 2)
    assert candidates(result, CellIds.R1C5) == [5, 6]
    assert candidates(result, CellIds.R1C6) == [5, 7]
    assert candidates(result, CellIds.R1C7) == [5, 6, 7, 8]
    assert candidates(result, CellIds.R1C8) == [6, 8, 9]
    assert candidates(result, CellIds.R1C9) == [7, 8, 9]
