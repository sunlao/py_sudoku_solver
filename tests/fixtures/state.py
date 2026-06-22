import pytest
from actors.state import State
from shared.models.constants import ActorNames, ActorDomainStatus
from shared.models.state import ActorDomainStates, ActorDomainState


@pytest.fixture
def state():
    return State


@pytest.fixture
def test_process_states() -> ActorDomainStates:
    return ActorDomainStates(
        states=(ActorDomainState(actor=ActorNames.BOARD, status=ActorDomainStatus.IDLE),)
    )
