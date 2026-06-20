from actors.state import State
from shared.models.constants import ActorNames, ProcessStatuses, ActorBehaviors
from shared.models.controller import ProcessState, ProcessStates
from shared.models.messages import (
    Message,
    ControllerStartup,
    GameStart,
    Board,
    Metadata,
)
from shared.models.side_effects import ActorSideEffects
from shared.models.static_data import Actors


class StartUp:

    def _actors(self, side_effects: ActorSideEffects, dto: Message) -> Actors:
        return side_effects.static_data(dto).controller_actors()

    def _game_start(self, dto: Board) -> Message[GameStart]:
        m = Metadata(actor_behavior=ActorBehaviors.GAME_START)
        return Message(metadata=m, content=GameStart(board=dto))

    def _process_states(self) -> ProcessStates:
        return ProcessStates(
            states=tuple(
                ProcessState(actor=a, status=self._status(a)) for a in ActorNames
            )
        )

    async def _send_start_game(
        self, side_effects: ActorSideEffects, dto: Message[GameStart]
    ) -> None:
        async with side_effects.transport_client(
            side_effects.fastapi_app, dto
        ) as client_api:
            await client_api.post("/", json=dto.model_dump(mode="json"))

    def _send_start_rbc(self) -> None:
        pass

    def _set_rbc_status(self) -> None:
        pass

    def _send_observer(self) -> None:
        pass

    @staticmethod
    def _status(name: str):
        if name is ActorNames.BOARD:
            return ProcessStatuses.IDLE
        return ProcessStatuses.STARTED

    @staticmethod
    def _transform_rbc(dto: Actors) -> Actors:
        return dto.model_copy(
            update={"actors": [a for a in dto.actors if a.rbc_flag is True]}
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ControllerStartup]
    ) -> None:
        states = self._process_states()
        State(dto).set_controller_process(states)
        actors = self._actors(side_effects, dto)
        game = self._game_start(dto.content.board)
        await self._send_start_game(side_effects, game)
        rbc = self._transform_rbc(actors)
        # print(f"**rbc {rbc}")
        print("**director end")
