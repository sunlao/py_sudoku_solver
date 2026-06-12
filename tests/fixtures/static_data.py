import pytest
from actors.actor_tasks.static_data.read import Read 

@pytest.fixture
def controller():
    return Read('controller').get_controller()