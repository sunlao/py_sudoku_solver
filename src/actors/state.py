from shared.models.constants import ActorBehaviors
from shared.models.controller import ProcessStates


class State:
    """Actor state is ephemeral and in-memory for the lifespan of the actor"""

    def __init__(self) -> None:
        self._cache: dict[ActorBehaviors, object] = {}

    def set_cached(self, key: ActorBehaviors, dto: object) -> None:
        self._cache[key] = dto

    def get_cached(self, key: ActorBehaviors) -> object | None:
        return self._cache.get(key)

    def set_controller_process(self, key: ActorBehaviors, dto: ProcessStates) -> None:
        self.set_cached(key, dto)
