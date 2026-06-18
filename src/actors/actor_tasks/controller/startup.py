from actors.static_data.read import Read
from actors.state import State
from shared.models.constants import StaticDataNames
from shared.models.constants import ActorNames, ProcessStatuses, ActorBehaviors
from shared.models.controller import ProcessState, ProcessStates
from shared.models.messages import (
    Message,
    ControllerStartup,
    GameStartup,
    Board,
    Metadata,
)
from shared.models.static_data import Actors, Actor


class Startup:

    def __init__(self) -> None:
        self.state = State()
        actors = Read(StaticDataNames.CONTROLLER).controller_actors()
        self.game = self._transform_game(actors)
        self.rbc = self._transform_rbc(actors)

    def _game_start(self, dto: Board) -> Message[GameStartup]:
        m = Metadata(actor_behavior=ActorBehaviors.GAME_START)
        return Message(metadata=m, content=(GameStartup(board=dto)))

    def _process_states(self) -> ProcessStates:
        return ProcessStates(
            states=tuple(
                ProcessState(actor=a, status=self._status(a)) for a in ActorNames
            )
        )

    def _message_game_start(self, dto: Message[GameStartup]) -> None:
        pass

    def _send_start_game(self) -> None:
        pass

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
    def _transform_game(dto: Actors) -> Actor:
        return next(a for a in dto.actors if a.name == ActorNames.GAME)

    @staticmethod
    def _transform_rbc(dto: Actors) -> Actors:
        return dto.model_copy(
            update={"actors": [a for a in dto.actors if a.rbc_flag is True]}
        )

    # pass when ready
    def director(self, dto: Message[ControllerStartup]) -> None:
        states = self._process_states()
        self.state.set_controller_process(dto.metadata.actor_behavior, states)
        print("**director end")
