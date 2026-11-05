from asyncio import wait_for
import pytest
from helpers.data import rbc_cells
from actors.actor_tasks.rbc.start import Start
from actors.actor_tasks.rbc.update import Update
from shared.models.constants import ActorBehaviors, ActorDomainStatus, ActorNames
from shared.models.messages import Message, Metadata


def assert_messages(messages, changed, status):
    expected_messages = {
        (cell.id, behavior)
        for cell in changed
        for behavior in (
            ActorBehaviors.GAME_UPDATE,
            ActorBehaviors(f"column{cell.column}.update"),
            ActorBehaviors(f"box{cell.box}.update"),
        )
    }
    cell_messages = [
        sent
        for sent in messages
        if sent.metadata.actor_behavior != ActorBehaviors.CONTROLLER_UPDATE_STATUS
    ]
    assert len(cell_messages) == len(expected_messages)
    assert {
        (sent.content.id, sent.metadata.actor_behavior) for sent in cell_messages
    } == expected_messages
    for sent in cell_messages:
        assert sent.content in changed
        assert sent.metadata.rbc_flag == (
            sent.metadata.actor_behavior != ActorBehaviors.GAME_UPDATE
        )

    statuses = [
        sent.content
        for sent in messages
        if sent.metadata.actor_behavior == ActorBehaviors.CONTROLLER_UPDATE_STATUS
    ]
    assert len(statuses) == 1
    assert len(messages) == len(cell_messages) + 1
    assert statuses[0].actor == ActorNames.ROW1
    assert statuses[0].status == status
    assert statuses[0].rbc_flag is True


@pytest.mark.parametrize(
    "scenario",
    (
        (Start, {}, (1, 2, 4, 6, 8, 9)),
        (Update, {"value": 4}, (1, 2, 6, 8, 9)),
        (Update, {"candidates": (1, 2)}, (1, 2, 4, 6, 8, 9)),
    ),
)
async def test_director(handler_solo, test_mailbox, startup_board, scenario):
    task_type, cell_update, candidates = scenario
    behavior = (
        ActorBehaviors.ROW1_START if task_type is Start else ActorBehaviors.ROW1_UPDATE
    )
    side_effects = handler_solo.actor_side_effects
    initial = rbc_cells(*startup_board.cells[:9])
    incoming = initial.cells[2].model_copy(update=cell_update)
    message = Message(
        metadata=Metadata(actor_behavior=behavior, rbc_flag=True),
        content=initial if task_type is Start else incoming,
    )
    if task_type is Update:
        side_effects.state.set_rbc_cells(message, initial)

    expected = initial.model_copy(
        update={
            "cells": tuple(
                (
                    cell
                    if cell.value is not None
                    else (
                        incoming
                        if task_type is Update and cell.id == incoming.id
                        else cell.model_copy(update={"candidates": candidates})
                    )
                )
                for cell in initial.cells
            )
        }
    )
    changed = tuple(
        new
        for old, new in zip(initial.cells, expected.cells, strict=True)
        if old != new
    )

    await task_type().director(side_effects, message)
    assert side_effects.state.get_cache(message) == expected
    assert initial.cells == startup_board.cells[:9]
    messages = [
        await wait_for(test_mailbox.dequeue(), timeout=1)
        for _ in range(3 * len(changed) + 1)
    ]
    assert_messages(messages, changed, ActorDomainStatus.WORKING)


@pytest.mark.parametrize(
    ("cell_index", "expected_status"),
    ((0, ActorDomainStatus.DONE), (2, ActorDomainStatus.IDLE)),
)
async def test_update_no_op(
    handler_solo,
    test_mailbox,
    startup_board,
    cell_index,
    expected_status,
):
    side_effects = handler_solo.actor_side_effects
    initial = rbc_cells(*startup_board.cells[:9])
    message = Message(
        metadata=Metadata(
            actor_behavior=ActorBehaviors.ROW1_UPDATE,
            rbc_flag=True,
        ),
        content=initial.cells[cell_index],
    )
    side_effects.state.set_rbc_cells(message, initial)

    await Update().director(side_effects, message)

    assert side_effects.state.get_cache(message) is initial
    sent = await wait_for(test_mailbox.dequeue(), timeout=1)
    assert sent.metadata.actor_behavior == ActorBehaviors.CONTROLLER_UPDATE_STATUS
    assert sent.content.actor == ActorNames.ROW1
    assert sent.content.status == expected_status
    assert sent.content.rbc_flag is True
