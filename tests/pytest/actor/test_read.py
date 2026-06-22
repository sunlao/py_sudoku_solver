from shared.models.constants import ActorNames


# Assert the controller static data
async def test_controller(controller):
    actors = controller.actors

    rbc = {a for a in actors if a.rbc_flag is True}
    game = [a for a in actors if a.name == ActorNames.GAME]
    board = [a for a in actors if a.name == ActorNames.BOARD]
    contrlr = [a for a in actors if a.name == ActorNames.CONTROLLER]

    assert len(actors) == 30
    assert len(contrlr) == 1
    assert len(game) == 1
    assert len(board) == 1
    assert len(rbc) == 27

    for actor in rbc:
        assert actor.name.startswith(("row", "box", "column"))
        assert actor.rbc_flag is True
        assert actor.domain_flag is True
        assert len(actor.cell_ids) == 9
    assert game[0].rbc_flag is False
    assert game[0].domain_flag is True
    assert game[0].cell_ids is None
    assert board[0].rbc_flag is False
    assert board[0].domain_flag is True
    assert board[0].cell_ids is None
    assert contrlr[0].rbc_flag is False
    assert contrlr[0].domain_flag is False
    assert contrlr[0].cell_ids is None
