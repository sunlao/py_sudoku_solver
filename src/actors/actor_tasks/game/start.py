from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from shared.models.constants import ActorDomainStatus
from shared.models.messages import GameStart, Message
from shared.models.side_effects import ActorSideEffects


class Start:
    async def director(
        self, side_effects: ActorSideEffects, dto: Message[GameStart]
    ) -> None:
        director_now = side_effects.now()
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        side_effects.state.set_game_board(dto, dto.content.board)
        msg = xform_update_state_msg(
            sending_actor=actor,
            sending_status=ActorDomainStatus.STARTED,
            last_director_timestamp=director_now,
            rbc_flag=False,
        )
        await send_update_msg(side_effects, msg)
        print("**director game:start end")
