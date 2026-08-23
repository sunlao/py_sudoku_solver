from datetime import datetime
from fastapi import status
from shared.models.constants import ActorBehaviors, ActorNames, ActorDomainStatus
from shared.models.messages import Message, Metadata
from shared.models.side_effects import ActorSideEffects
from shared.models.state import ActorDomainState


async def post_controller_msg(
    side_effects: ActorSideEffects, dto: Message[ActorDomainState]
) -> None:
    """post ActorDomainState update message to a dynamicaly generated route from dto.metadata.actor_behavior
    - /address/v1/{actor}/{behavior}
    """
    async with side_effects.transport_client(side_effects.fastapi_app, dto) as client:
        response = await client.post("/", json=dto.model_dump(mode="json"))
        if response.status_code != status.HTTP_202_ACCEPTED:
            raise RuntimeError(
                f"{dto.metadata.actor_behavior} failed to send "
                f"MessageID: {dto.metadata.message_id}"
            )


def controller_msg(
    sending_actor: ActorNames,
    sending_status: ActorDomainStatus,
    last_director_timestamp: datetime,
    rbc_flag: bool,
) -> Message[ActorDomainState]:
    """Build controller ActorDomainState update message"""
    return Message[ActorDomainState](
        metadata=Metadata(actor_behavior=ActorBehaviors.CONTROLLER_UPDATE_STATUS),
        content=ActorDomainState(
            actor=sending_actor,
            status=sending_status,
            last_director_timestamp=last_director_timestamp,
            rbc_flag=rbc_flag,
        ),
    )
