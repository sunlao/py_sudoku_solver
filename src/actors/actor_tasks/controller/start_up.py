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
    RBCStart,
)
from shared.models.side_effects import ActorSideEffects
from shared.models.static_data import Actors, Actor


class StartUp:

    def _get_actors(self, side_effects: ActorSideEffects, dto: Message) -> Actors:
        return side_effects.static_data(dto).controller_actors()

    async def _send_start_game(
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
        self, side_effects: ActorSideEffects, dto: Message[RBCStart]
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

    async def _settup_gather_xform_rbc_start(
        self, side_effects: ActorSideEffects, dto: Board, actors: Actors
    ) -> None:
        msgs = tuple(
            self._xform_rbc_start(dto, a) for a in actors.actors if a.rbc_flag is True
        )
        await side_effects.gather(
            *(self._send_rbc_start(side_effects, msg) for msg in msgs)
        )

    @staticmethod
    def _status(actor: Actor):
        if actor.name == ActorNames.BOARD:
            return ActorDomainStatus.IDLE
        return ActorDomainStatus.INIT

    def _xform_actor_domain_states(
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

    def _xform_game_start(self, dto: Board) -> Message[GameStart]:
        m = Metadata(actor_behavior=ActorBehaviors.GAME_START)
        return Message(metadata=m, content=GameStart(board=dto))

    def _xform_rbc_start(self, dto: Board, actor: Actor) -> Message[RBCStart]:
        m = Metadata(actor_behavior=ActorBehaviors(f"{actor.name}.start"))
        ids = set(actor.cell_ids)
        c = tuple(c for c in dto.cells if c.id in ids)
        return Message(metadata=m, content=RBCStart(actor=actor.name, cells=c))

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ControllerStartup]
    ) -> None:
        director_now = side_effects.now()
        actors = self._get_actors(side_effects, dto)
        ads = self._xform_actor_domain_states(actors, director_now)
        side_effects.state.set_actor_domain_states(dto, ads)
        game = self._xform_game_start(dto.content.board)
        await side_effects.gather(
            self._send_start_game(side_effects, game),
            self._settup_gather_xform_rbc_start(
                side_effects, dto.content.board, actors
            ),
        )
        print("**director controller: start-up end ")
