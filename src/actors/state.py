from shared.models.constants import StateKeys
from shared.models.controller import ProcessStates


class State:
    """Actor state is ephemeral and in-memory for the lifespan of the actor"""

    def __init__(self) -> None:
        self._cache: dict[StateKeys, object] = {}

    def set_cached(self, key: StateKeys, dto: object) -> None:
        self._cache[key] = dto

    def get_cached(self, key: StateKeys) -> object | None:
        return self._cache.get(key)

    def set_controller_process(self, dto: ProcessStates) -> None:
        self.set_cached(StateKeys.CONTROLLER_PROCESS_STATE, dto)

    def get_controller_process(self) -> ProcessStates | None:
        return self.get_cached(StateKeys.CONTROLLER_PROCESS_STATE)
