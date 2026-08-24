from datetime import datetime
from actors.actor_tasks.send import Send
from shared.models.constants import ActorDomainStatus
from shared.models.messages import GameStart, Message
from shared.models.side_effects import ActorSideEffects, PostControllerUpdate


class Start:

    def __init__(self):
        self.send = Send()

    async def _send_controller(
            self, 
            side_effects: ActorSideEffects, 
            dto: Message[GameStart], 
            director_now: datetime
        ) -> None:
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        dto = PostControllerUpdate(
            side_effects=side_effects, 
            sending_actor=actor,
            sending_status=ActorDomainStatus.STARTED,
            last_director_timestamp=director_now,
            rbc_flag=False
        )
        await self.send.post_controller_update(dto)

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[GameStart]
    ) -> None:
        director_now = side_effects.now()
        side_effects.state.set_game_board(dto, dto.content.board)
        self._send_controller(side_effects, dto, director_now)
        print("**director game:start end")
