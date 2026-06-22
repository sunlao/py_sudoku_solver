from fastapi import status
from actors.state import State
from shared.models.constants import ActorNames, ActorDomainStatus, ActorBehaviors
from shared.models.state import ActorDomainState, ActorDomainStates
from shared.models.messages import (
    Message,
    ControllerStartup,
    GameStart,
    Board,
    Metadata,
)
from shared.models.side_effects import ActorSideEffects
from shared.models.static_data import Actors, Actor


class StartUp:

    def _get_actors(self, side_effects: ActorSideEffects, dto: Message) -> Actors:
        return side_effects.static_data(dto).controller_actors()

    def _get_actor_domain_states(self, dto: Actors) -> ActorDomainStates:
        return ActorDomainStates(
            states=tuple(
                ActorDomainState(actor=a.name, status=self._status(a))
                for a in dto.actors
                if a.process_flag is True
            )
        )

    def _get_game_start(self, dto: Board) -> Message[GameStart]:
        m = Metadata(actor_behavior=ActorBehaviors.GAME_START)
        return Message(metadata=m, content=GameStart(board=dto))

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

    def _send_start_rbc(self) -> None:
        pass

    def _set_rbc_status(self) -> None:
        pass

    def _send_observer(self) -> None:
        pass

    @staticmethod
    def _status(actor: Actor):
        if actor.name == ActorNames.BOARD:
            return ActorDomainStatus.IDLE
        return ActorDomainStatus.STARTED

    @staticmethod
    def _transform_rbc(dto: Actors) -> Actors:
        return dto.model_copy(
            update={"actors": [a for a in dto.actors if a.rbc_flag is True]}
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ControllerStartup]
    ) -> None:
        actors = self._get_actors(side_effects, dto)
        states = self._get_actor_domain_states(actors)
        State(dto).set_actor_domain_states(states)
        game = self._get_game_start(dto.content.board)
        await self._send_start_game(side_effects, game)
        # rbc = self._transform_rbc(actors)
        # print(f"**rbc {rbc}")
        print("**director end")
