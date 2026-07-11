from shared.models.constants import CellIds
from shared.models.board import ActorBehaviors


# Assert the controller static data
async def test_maps(cell_behaviors):
    maps = cell_behaviors.maps
    assert len(maps) == 81
    assert len({m.id for m in maps}) == 81
    assert all(len(m.behaviors) == 3 for m in maps)

    r1c1 = next(m for m in maps if m.id == CellIds.R1C1)
    assert r1c1.behaviors == (
        ActorBehaviors.ROW1_EVAL,
        ActorBehaviors.COLUMN1_EVAL,
        ActorBehaviors.BOX1_EVAL,
    )

    r5c5 = next(m for m in maps if m.id == CellIds.R5C5)
    assert r5c5.behaviors == (
        ActorBehaviors.ROW5_EVAL,
        ActorBehaviors.COLUMN5_EVAL,
        ActorBehaviors.BOX5_EVAL,
    )

    r9c9 = next(m for m in maps if m.id == CellIds.R9C9)
    assert r9c9.behaviors == (
        ActorBehaviors.ROW9_EVAL,
        ActorBehaviors.COLUMN9_EVAL,
        ActorBehaviors.BOX9_EVAL,
    )
