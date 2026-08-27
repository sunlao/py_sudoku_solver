from datetime import datetime
from actors.actor_tasks.send import Send
from shared.models.constants import ActorNames, ActorDomainStatus
from shared.models.state import ActorDomainState, ActorDomainStates
from shared.models.messages import Board, ControllerStartup, Message
from shared.models.side_effects import ActorSideEffects
from shared.models.static_data import Actors, Actor


class StartUp:

    def __init__(self):
        self.send = Send()

    def _domain_actors_state(self, dto: Actors, ts: datetime) -> ActorDomainStates:
        return ActorDomainStates(
            states=tuple(
                ActorDomainState(
                    actor=a.name,
                    status=self._status(a),
                    last_director_timestamp=ts,
                    rbc_flag=a.rbc_flag,
                )
                for a in dto.actors
                if a.domain_flag is True
            )
        )

    async def _gather_send_rbc_msgs(
        self, side_effects: ActorSideEffects, dto: Board, actors: Actors
    ) -> None:
        msgs = tuple(
            self.send.msg_rbc_init_board(dto, a)
            for a in actors.actors
            if a.rbc_flag is True
        )
        await side_effects.gather(
            *(self.send.post_rbc_init(side_effects, m) for m in msgs)
        )

    @staticmethod
    def _status(actor: Actor):
        if actor.name == ActorNames.BOARD:
            return ActorDomainStatus.IDLE
        return ActorDomainStatus.STARTING

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ControllerStartup]
    ) -> None:
        now = side_effects.now()
        actors = side_effects.static_data(dto).controller_actors()
        state = self._domain_actors_state(actors, now)
        side_effects.state.set_domain_actors_state(dto, state)
        await side_effects.gather(
            self.send.post_game_start(side_effects, dto.content.board),
            self._gather_send_rbc_msgs(side_effects, dto.content.board, actors),
        )
        print("**director controller: start-up end ")
