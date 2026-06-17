import pytest
from actors.static_data.read import Read
from shared.models.constants import StaticDataNames
from shared.models.static_data import Actors


@pytest.fixture
def controller() -> Actors:
    return Read(StaticDataNames.CONTROLLER).controller_actors()
