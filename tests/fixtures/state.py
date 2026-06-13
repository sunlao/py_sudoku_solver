import pytest
from actors.state import State
from shared.models.constants import ActorNames, ProcessStatuses
from shared.models.controller import ProcessStates, ProcessState


@pytest.fixture
def state():
    return State()


@pytest.fixture
def test_process_states() -> ProcessStates:
    return ProcessStates(
        states=(ProcessState(actor=ActorNames.BOARD, status=ProcessStatuses.IDLE),)
    )
