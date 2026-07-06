from helpers.algorithms import candidates, cell, rbc_cells, value
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
    result = rbc_algorithms.hidden(cells, 1)
    assert value(result, CellIds.R1C9) == 9
    assert candidates(result, CellIds.R1C9) == [9]


def test_size_2(rbc_algorithms):
    row1_cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None),
    )
    row1_results = rbc_algorithms.hidden(row1_cells, 2)
    assert candidates(row1_results, CellIds.R1C5) == [5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C6) == [5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C7) == [5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C8) == [5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C9) == [5, 6, 7, 8, 9]
    col5_cells = rbc_cells(
        cell(row1_results, CellIds.R1C5),
        Cell(id=CellIds.R2C5, row=2, column=5, box=2, value=1),
        Cell(id=CellIds.R3C5, row=3, column=5, box=2, value=2),
        Cell(id=CellIds.R4C5, row=4, column=5, box=5, value=3),
        Cell(id=CellIds.R5C5, row=5, column=5, box=5, value=4),
        Cell(id=CellIds.R6C5, row=6, column=5, box=5, value=8),
        Cell(id=CellIds.R7C5, row=7, column=5, box=8, value=9),
        Cell(id=CellIds.R8C5, row=8, column=5, box=8, value=None),
        Cell(id=CellIds.R9C5, row=9, column=5, box=8, value=None),
    )
    col5_results = rbc_algorithms.hidden(col5_cells, 2)
    assert candidates(col5_results, CellIds.R1C5) == [5, 6, 7]
    assert candidates(col5_results, CellIds.R8C5) == [5, 6, 7]
    assert candidates(col5_results, CellIds.R9C5) == [5, 6, 7]


def test_size_3(rbc_algorithms):
    row1_cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=None),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=None),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None),
    )
    row1_results = rbc_algorithms.hidden(row1_cells, 3)
    assert candidates(row1_results, CellIds.R1C3) == [3, 4, 5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C4) == [3, 4, 5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C5) == [3, 4, 5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C6) == [3, 4, 5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C7) == [3, 4, 5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C8) == [3, 4, 5, 6, 7, 8, 9]
    assert candidates(row1_results, CellIds.R1C9) == [3, 4, 5, 6, 7, 8, 9]
    box2_cells = rbc_cells(
        Cell(id=CellIds.R2C4, row=2, column=4, box=2, value=1),
        Cell(id=CellIds.R2C5, row=2, column=5, box=2, value=2),
        Cell(id=CellIds.R2C6, row=2, column=6, box=2, value=9),
        Cell(id=CellIds.R3C4, row=3, column=4, box=2, value=6),
        Cell(id=CellIds.R3C5, row=3, column=5, box=2, value=7),
        Cell(id=CellIds.R3C6, row=3, column=6, box=2, value=8),
        cell(row1_results, CellIds.R1C4),
        cell(row1_results, CellIds.R1C5),
        cell(row1_results, CellIds.R1C6),
    )
    box2_results = rbc_algorithms.hidden(box2_cells, 3)
    assert candidates(box2_results, CellIds.R1C4) == [3, 4, 5]
    assert candidates(box2_results, CellIds.R1C5) == [3, 4, 5]
    assert candidates(box2_results, CellIds.R1C6) == [3, 4, 5]


def test_no_hidden_found(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None),
    )
    result = rbc_algorithms.hidden(cells, 2)
    assert candidates(result, CellIds.R1C5) == [5, 6, 7, 8, 9]
    assert candidates(result, CellIds.R1C6) == [5, 6, 7, 8, 9]
    assert candidates(result, CellIds.R1C7) == [5, 6, 7, 8, 9]
    assert candidates(result, CellIds.R1C8) == [5, 6, 7, 8, 9]
    assert candidates(result, CellIds.R1C9) == [5, 6, 7, 8, 9]


def test_not_needed_no_hidden(rbc_algorithms):
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
    result = rbc_algorithms.hidden(cells, 2)
    assert candidates(result, CellIds.R1C5) == [5, 6]
    assert candidates(result, CellIds.R1C6) == [5, 6]
    assert candidates(result, CellIds.R1C7) == [7, 8, 9]
    assert candidates(result, CellIds.R1C8) == [7, 8, 9]
    assert candidates(result, CellIds.R1C9) == [7, 8, 9]


def test_not_needed_too_many_cells(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(5, 6, 7)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(5, 6, 8)),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(5, 6, 9)),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(7, 8, 9)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(7, 8, 9)),
    )
    result = rbc_algorithms.hidden(cells, 2)
    assert candidates(result, CellIds.R1C5) == [5, 6, 7]
    assert candidates(result, CellIds.R1C6) == [5, 6, 8]
    assert candidates(result, CellIds.R1C7) == [5, 6, 9]
    assert candidates(result, CellIds.R1C8) == [7, 8, 9]
    assert candidates(result, CellIds.R1C9) == [7, 8, 9]


def test_not_needed_too_few_cells(rbc_algorithms):
    cells = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=None, candidates=(5, 6, 7)),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=None, candidates=(7, 8, 9)),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=None, candidates=(7, 8, 9)),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None, candidates=(7, 8, 9)),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None, candidates=(7, 8, 9)),
    )
    result = rbc_algorithms.hidden(cells, 2)
    assert candidates(result, CellIds.R1C5) == [5, 6, 7]
    assert candidates(result, CellIds.R1C6) == [7, 8, 9]
    assert candidates(result, CellIds.R1C7) == [7, 8, 9]
    assert candidates(result, CellIds.R1C8) == [7, 8, 9]
    assert candidates(result, CellIds.R1C9) == [7, 8, 9]
