import pytest
from api.v1.helpers.messages import start_up
from shared.models.messages import MessageSend, Board


@pytest.fixture
def startup_message(startup_board: Board) -> MessageSend:
    return start_up(startup_board)
