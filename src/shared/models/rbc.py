from datetime import datetime
from pydantic import BaseModel
from shared.models.policy import DTO_CONFIG
from shared.models.side_effects import ActorSideEffects
from shared.models.constants import ActorNames


class ControllerMessageInput(BaseModel):
    model_config = DTO_CONFIG
    side_effects: ActorSideEffects
    actor_name: ActorNames
    director_now: datetime
