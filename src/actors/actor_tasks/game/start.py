from actors.actor_tasks.shared import send_update_msg, xform_update_state_msg
from shared.models.constants import ActorBehaviors, ActorNames, ActorDomainStatus
from shared.models.messages import GameStart, Message
from shared.models.side_effects import ActorSideEffects


class Start:
    async def director(
        self, side_effects: ActorSideEffects, dto: Message[GameStart]
    ) -> None:
        director_now = side_effects.now()
        side_effects.state.set_game_board(dto, dto.content.board)
        msg = xform_update_state_msg(
            ActorBehaviors.CONTROLLER_UPDATE_STATUS,
            ActorNames.GAME,
            ActorDomainStatus.STARTED,
            director_now,
            False,
        )
        await send_update_msg(side_effects, msg)
        print("**director game:start end")
