import pytest
from api.v1.helpers.messages import start_up
from shared.models.messages import Message, Board


@pytest.fixture
def startup_message(startup_board: Board) -> Message:
    return start_up(startup_board)
