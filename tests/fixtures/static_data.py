import pytest
from actors.static_data.read import Read
from shared.models.static_data import Actors


@pytest.fixture
def controller(startup_message) -> Actors:
    return Read(startup_message).controller_actors()
