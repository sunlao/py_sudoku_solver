import pytest
from actors.static_data.read import Read
from shared.models.board import CellBehaviorMaps
from shared.models.static_data import Actors


@pytest.fixture
def cell_behaviors(startup_rbc_message) -> CellBehaviorMaps:
    return Read(startup_rbc_message).rbc_cell_behavior_maps()


@pytest.fixture
def controller(startup_message) -> Actors:
    return Read(startup_message).controller_actors()
