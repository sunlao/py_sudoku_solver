from datetime import datetime
from shared.models.policy import DTO_CONFIG
from uuid import UUID
from pydantic import BaseModel
from shared.models.constants import ActorBehaviors, MessageType


class DomainActorStatus(BaseModel):
    """Metadata wrapper for all messages"""

    model_config = DTO_CONFIG
    message_id: UUID
    type: MessageType
    start_time: datetime
    end_time: datetime
    actor_behavior: ActorBehaviors
