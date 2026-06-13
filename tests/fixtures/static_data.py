import pytest
from actors.static_data.read import Read 

@pytest.fixture
def controller():
    return Read('controller').controller()