from actors.actor_tasks.send import Send
from shared.models.constants import ActorDomainStatus
from shared.models.messages import GameStart, Message
from shared.models.side_effects import ActorSideEffects


class Start:

    def __init__(self):
        self.send = Send()

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[GameStart]
    ) -> None:
        director_now = side_effects.now()
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        side_effects.state.set_game_board(dto, dto.content.board)
        await self.send.post_controller_update(
            side_effects,
            sending_actor=actor,
            sending_status=ActorDomainStatus.STARTED,
            last_director_timestamp=director_now,
            rbc_flag=False,
        )
        print("**director game:start end")
