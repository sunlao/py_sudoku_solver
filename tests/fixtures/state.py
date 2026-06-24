import pytest
from actors.state import State
from shared.models.constants import ActorNames, ActorDomainStatus
from shared.models.state import ActorDomainStates, ActorDomainState


@pytest.fixture
def state():
    return State()


@pytest.fixture
def test_actor_domain_state() -> ActorDomainStates:
    return ActorDomainStates(
        states=(
            ActorDomainState(
                actor=ActorNames.BOARD, rbc_flag=False, status=ActorDomainStatus.IDLE
            ),
        )
    )
