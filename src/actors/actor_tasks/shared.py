from datetime import datetime
from fastapi import status
from shared.models.constants import ActorBehaviors, ActorNames, ActorDomainStatus
from shared.models.messages import Message, Metadata
from shared.models.side_effects import ActorSideEffects
from shared.models.state import ActorDomainState


async def send_update_msg(
    side_effects: ActorSideEffects, message_dto: Message[ActorDomainState]
) -> None:
    async with side_effects.transport_client(
        side_effects.fastapi_app, message_dto
    ) as client_api:
        response = await client_api.post("/", json=message_dto.model_dump(mode="json"))
        if response.status_code != status.HTTP_202_ACCEPTED:
            raise RuntimeError(
                f"{message_dto.metadata.actor_behavior} failed to send "
                f"MessageID: {message_dto.metadata.message_id}"
            )


def xform_update_state_msg(
    recieving_actor_behavior: ActorBehaviors,
    sending_actor: ActorNames,
    status: ActorDomainStatus,
    last_director_timestamp: datetime,
    rbc_flag: bool,
) -> Message[ActorDomainState]:
    return Message[ActorDomainState](
        metadata=Metadata(actor_behavior=recieving_actor_behavior),
        content=ActorDomainState(
            actor=sending_actor,
            status=status,
            last_director_timestamp=last_director_timestamp,
            rbc_flag=rbc_flag,
        ),
    )
