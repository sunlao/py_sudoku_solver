import pytest
from api.v1.helpers.messages import start_up
from shared.models.constants import ActorBehaviors, MessageType
from shared.models.messages import Message, Board


@pytest.fixture
def startup_message(startup_board: Board) -> Message:
    m = start_up(startup_board)
    return m.model_copy(
        update={
            "metadata": m.metadata.model_copy(
                update={
                    "actor_behavior": ActorBehaviors.CONTROLLER_START_UP,
                    "type": MessageType.TEST,
                }
            )
        }
    )


@pytest.fixture
def startup_rbc_message(startup_board: Board) -> Message:
    m = start_up(startup_board)
    return m.model_copy(
        update={
            "metadata": m.metadata.model_copy(
                update={
                    "actor_behavior": ActorBehaviors.ROW1_START_UP,
                    "type": MessageType.TEST,
                    "rbc_flag": True,
                }
            )
        }
    )


@pytest.fixture
def bad_message(startup_board: Board) -> Message:
    m = start_up(startup_board)
    return m.model_copy(
        update={
            "metadata": m.metadata.model_copy(
                update={
                    "actor_behavior": ActorBehaviors.TEST_BAD,
                    "type": MessageType.TEST,
                }
            )
        }
    )
