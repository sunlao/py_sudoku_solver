import pytest
from actors.actor_tasks.rbc.helpers.algorithms import Algorithms


@pytest.fixture
def rbc_algorithms():
    return Algorithms()
