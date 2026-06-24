from fastapi import status
from shared.models.constants import ActorBehaviors
from shared.models.messages import GameStart, Message, ActorDomainUpdate, Metadata
from shared.models.side_effects import ActorSideEffects


class Start:

    async def _send_update_process(
        self, side_effects: ActorSideEffects, dto: Message[ActorDomainUpdate]
    ) -> None:
        async with side_effects.transport_client(
            side_effects.fastapi_app, dto
        ) as client_api:
            response = await client_api.post("/", json=dto.model_dump(mode="json"))
            if response.status_code != status.HTTP_202_ACCEPTED:
                raise RuntimeError(
                    f"{dto.metadata.actor_behavior} failed to send "
                    f"MessageID: {dto.metadata.message_id}"
                )

    def _xform_actor_domain_update(self, dto: Message[GameStart]) -> Message[ActorDomainUpdate]:
        return Message(
            metadata=Metadata(actor_behavior=ActorBehaviors.CONTROLLER_UPDATE_STATUS),
            content=ActorDomainUpdate(start_metadata=dto.metadata, start_content=dto.content),
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[GameStart]
    ) -> None:
        side_effects.state.set_game_board(dto, dto.content.board)
        actor_domain_update = self._xform_actor_domain_update(dto)
        await self._send_update_process(side_effects, actor_domain_update)
        print("**director game:start end")
