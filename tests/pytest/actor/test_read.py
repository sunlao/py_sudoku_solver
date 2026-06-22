from shared.models.constants import ActorNames


# Assert the controller static data has 29 actors
# 1 game and board + 27 RBC actors
# all actors have two adresses except board which has 1
# address starts with address + actor name
async def test_controller(controller):
    actors = controller.actors

    rbc = {a for a in actors if a.name.startswith(("row", "box", "column"))}
    game = [a for a in actors if a.name == ActorNames.GAME]
    board = [a for a in actors if a.name == ActorNames.BOARD]
    contrlr = [a for a in actors if a.name == ActorNames.CONTROLLER]

    assert len(actors) == 30
    assert len(contrlr) == 1
    assert len(game) == 1
    assert len(board) == 1
    assert len(rbc) == 27

    for actor in rbc:
        assert actor.rbc_flag is True
        assert len(actor.cells) == 9
    assert game[0].rbc_flag is False
    assert game[0].cells is None
    assert board[0].rbc_flag is False
    assert board[0].cells is None
    assert contrlr[0].rbc_flag is False
    assert contrlr[0].cells is None
