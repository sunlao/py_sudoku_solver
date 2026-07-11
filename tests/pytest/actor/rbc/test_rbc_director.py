from helpers.data import rbc_cells
from actors.actor_tasks.rbc.eval import Eval
from shared.models.constants import ActorBehaviors
from shared.models.messages import Message, Metadata, Cell, CellIds

rbc_eval = Eval()


# pylint: disable=protected-access
async def test_state(handler_solo, startup_message, test_actor_domain_state):
    side_effects = handler_solo.actor_side_effects
    side_effects.fastapi_app.state.actor_state.set_actor_domain_states(
        startup_message,
        test_actor_domain_state,
    )
    rbc_init = rbc_cells(
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
    expected = await rbc_eval._eval_all(side_effects, rbc_init)
    cell9 = next((c for c in expected.cells if c.id == CellIds.R1C9))
    assert cell9.value == 9
    message = Message(
        metadata=Metadata(
            actor_behavior=ActorBehaviors.ROW1_EVAL,
            rbc_flag=True,
        ),
        content=rbc_init,
    )
    await rbc_eval.director(side_effects, message)
    result = side_effects.state.get_cache(message)
    assert result == expected

    rbc = rbc_cells(
        Cell(id=CellIds.R1C1, row=1, column=1, box=1, value=1),
        Cell(id=CellIds.R1C2, row=1, column=2, box=1, value=2),
        Cell(id=CellIds.R1C3, row=1, column=3, box=1, value=3),
        Cell(id=CellIds.R1C4, row=1, column=4, box=2, value=4),
        Cell(id=CellIds.R1C5, row=1, column=5, box=2, value=5),
        Cell(id=CellIds.R1C6, row=1, column=6, box=2, value=6),
        Cell(id=CellIds.R1C7, row=1, column=7, box=3, value=7),
        Cell(id=CellIds.R1C8, row=1, column=8, box=3, value=None),
        Cell(id=CellIds.R1C9, row=1, column=9, box=3, value=9),
    )
    expected = await rbc_eval._eval_all(side_effects, rbc)
    cell8 = next((c for c in expected.cells if c.id == CellIds.R1C8))
    assert cell8.value == 8
    message = Message(
        metadata=Metadata(
            actor_behavior=ActorBehaviors.ROW1_EVAL,
            rbc_flag=True,
        ),
        content=rbc,
    )
    await rbc_eval.director(side_effects, message)
    result = side_effects.state.get_cache(message)
    assert result == expected
