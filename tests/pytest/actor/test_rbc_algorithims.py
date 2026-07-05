from shared.models.messages import RBCCells, Cell, ActorNames, CellIds

def test_hidden_1(rbc_algorithms):
    test1 = RBCCells(
        actor=ActorNames.ROW1,
        cells=(
            Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
            Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
            Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
            Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
            Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=5),
            Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=6),
            Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=7),
            Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=8),
            Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=None), 
        ),
    )
    result1 = rbc_algorithms.naked_subset(test1, 1)
    result2 = rbc_algorithms.hidden_subset(test1, 1)
    res_cell1 = next(c for c in result1.cells if c.id == CellIds.R1C9)
    res_cell2 = next(c for c in result2.cells if c.id == CellIds.R1C9)
    print(f"\nres_cell1: {res_cell1}")
    print(f"\nres_cell2: {res_cell2}")
    # assert result
