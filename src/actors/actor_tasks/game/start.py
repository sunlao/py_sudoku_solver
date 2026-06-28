from datetime import datetime
from fastapi import status
from shared.models.constants import ActorBehaviors, ActorNames, ActorDomainStatus
from shared.models.messages import GameStart, Message, Metadata
from shared.models.side_effects import ActorSideEffects
from shared.models.state import ActorDomainState


class Start:

    async def _send_update_msg(
        self, side_effects: ActorSideEffects, dto: Message[ActorDomainState]
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

    def _xform_update_state_msg(self, ts: datetime) -> Message[ActorDomainState]:
        return Message[ActorDomainState](
            metadata=Metadata(actor_behavior=ActorBehaviors.CONTROLLER_UPDATE_STATUS),
            content=ActorDomainState(
                actor=ActorNames.GAME,
                status=ActorDomainStatus.STARTED,
                last_director_timestamp=ts,
                rbc_flag=False,
            ),
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[GameStart]
    ) -> None:
        director_now = side_effects.now()
        side_effects.state.set_game_board(dto, dto.content.board)
        msg = self._xform_update_state_msg(director_now)
        print(f"msg content actor: {msg.content.actor}")
        await self._send_update_msg(side_effects, msg)
        print("**director game:start end")
