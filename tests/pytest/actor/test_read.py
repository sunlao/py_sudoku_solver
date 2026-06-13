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

    assert len(actors) == 29
    assert len(game) == 1
    assert len(board) == 1
    assert len(rbc) == 27

    for actor in rbc:
        assert actor.rbc_flag is True
        assert len(actor.addresses) == 2
        for address in actor.addresses:
            assert address.startswith("address/" + actor.name)
    assert len(game[0].addresses) == 2
    assert game[0].rbc_flag is False
    for address in game[0].addresses:
        assert address.startswith("address/" + game[0].name)
    assert len(board[0].addresses) == 1
    assert board[0].rbc_flag is False
    for address in board[0].addresses:
        assert address.startswith("address/" + board[0].name)
