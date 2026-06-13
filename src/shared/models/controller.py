from datetime import datetime, UTC
from pydantic import BaseModel, Field
from shared.models.constants import ActorNames, ProcessStatuses
from shared.models.policy import DTO_CONFIG


class ProcessState(BaseModel):
    """Controller process state for an actor"""

    model_config = DTO_CONFIG

    actor: ActorNames
    status: ProcessStatuses
    time: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ProcessStates(BaseModel):
    """Controller process state for all actors"""

    model_config = DTO_CONFIG

    states: tuple[ProcessState, ...]
