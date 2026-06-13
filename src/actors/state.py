from functools import cache
from shared.models.controller import ProcessStates


class State:
    """Actor state is ephemeral and in-memory for the lifespan of the actor"""

    def __init__(self) -> None:
        self.controller_process_state = None

    @cache
    def _cache(self, cache):
        return cache

    def set_controller_process(self, dto: ProcessStates) -> None:
        self.controller_process_state = dto
        self._cache(self.controller_process_state)

    def get_controller_process(self) -> ProcessStates:
        return self._cache(self.controller_process_state)
