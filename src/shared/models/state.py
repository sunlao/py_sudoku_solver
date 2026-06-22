from datetime import datetime, UTC
from pydantic import BaseModel, Field
from shared.models.constants import ActorNames, ActorDomainStatus
from shared.models.policy import DTO_CONFIG


class ActorDomainState(BaseModel):
    """Controller process state for an actor"""

    model_config = DTO_CONFIG

    actor: ActorNames
    rbc_flag: bool
    status: ActorDomainStatus
    time: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ActorDomainStates(BaseModel):
    """Controller process state for all actors"""

    model_config = DTO_CONFIG

    states: tuple[ActorDomainState, ...]
