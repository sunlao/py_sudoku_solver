from shared.models.constants import StaticDataNames
from shared.models.constants import ActorNames, ProcessStatuses
from shared.models.controller import ProcessState, ProcessStates
from shared.models.messages import Message
from shared.models.static_data import Actors, Actor
from actors.static_data.read import Read


class Startup:

    def __init__(self) -> None:
        actors = Read(StaticDataNames.CONTROLLER).controller()
        self.game = self._transform_game(actors)
        self.rbc = self._transform_rbc(actors)

    def _process_states(self) -> ProcessStates:
        return ProcessStates(
            states=tuple(
                ProcessState(actor=a, status=self._status(a)) for a in ActorNames
            )
        )

    def _set_process(self, states: ProcessStates) -> None:
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

    def director(self, message: Message) -> None:
        states = self._process_states()
