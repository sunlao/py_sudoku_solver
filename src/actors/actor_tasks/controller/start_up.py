from datetime import datetime
from fastapi import status
from shared.models.constants import ActorNames, ActorDomainStatus, ActorBehaviors
from shared.models.state import ActorDomainState, ActorDomainStates
from shared.models.messages import (
    Board,
    ControllerStartup,
    GameStart,
    Message,
    Metadata,
    RBCCells,
)
from shared.models.side_effects import ActorSideEffects
from shared.models.static_data import Actors, Actor


class StartUp:

    def _domain_actors_state(
        self, dto: Actors, ts: datetime
    ) -> ActorDomainStates:
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
            self._msg_rbc_start(dto, a) for a in actors.actors if a.rbc_flag is True
        )
        await side_effects.gather(
            *(self._send_rbc_start(side_effects, msg) for msg in msgs)
        )

    def _msg_game_start(self, dto: Board) -> Message[GameStart]:
        m = Metadata(actor_behavior=ActorBehaviors.GAME_START)
        return Message(metadata=m, content=GameStart(board=dto))

    def _msg_rbc_start(self, dto: Board, actor: Actor) -> Message[RBCCells]:
        m = Metadata(
            actor_behavior=ActorBehaviors(f"{actor.name}.start-up"), rbc_flag=True
        )
        ids = set(actor.cell_ids)
        c = tuple(c for c in dto.cells if c.id in ids)
        return Message(metadata=m, content=RBCCells(actor=actor.name, cells=c))

    async def _send_game_msg(
        self, side_effects: ActorSideEffects, dto: Message[GameStart]
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

    async def _send_rbc_start(
        self, side_effects: ActorSideEffects, dto: Message[RBCCells]
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

    @staticmethod
    def _status(actor: Actor):
        if actor.name == ActorNames.BOARD:
            return ActorDomainStatus.IDLE
        return ActorDomainStatus.INIT

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ControllerStartup]
    ) -> None:
        now = side_effects.now()
        actors = side_effects.static_data(dto).controller_actors()
        state = self._domain_actors_state(actors, now)
        side_effects.state.set_domain_actors_state(dto, state)
        msg_game = self._msg_game_start(dto.content.board)
        await side_effects.gather(
            self._send_game_msg(side_effects, msg_game),
            self._gather_send_rbc_msgs(
                side_effects, dto.content.board, actors
            ),
        )
        print("**director controller: start-up end ")
