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
        assert len(actor.behaviors) == 2
        for behavior in actor.behaviors:
            assert behavior in ("start", "cell-update")
    assert len(game[0].behaviors) == 2
    assert game[0].rbc_flag is False
    for behavior in game[0].behaviors:
        assert behavior in ("start", "cell-update")
    assert len(board[0].behaviors) == 1
    assert board[0].rbc_flag is False
    for behavior in board[0].behaviors:
        assert behavior == "initialize"
    assert len(contrlr[0].behaviors) == 3
    assert contrlr[0].rbc_flag is False
    for behavior in contrlr[0].behaviors:
        assert behavior in ("start-up", "rbc-status", "update-process")
