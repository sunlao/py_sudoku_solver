from datetime import datetime
from pydantic import BaseModel
from shared.models.constants import ActorNames, ActorDomainStatus
from shared.models.policy import DTO_CONFIG


class ActorDomainState(BaseModel):
    """Controller process state for an actor"""

    model_config = DTO_CONFIG

    actor: ActorNames
    status: ActorDomainStatus
    last_director_timestamp: datetime
    rbc_flag: bool


class ActorDomainStates(BaseModel):
    """Controller process state for all actors"""

    model_config = DTO_CONFIG

    states: tuple[ActorDomainState, ...]
