from shared.models.constants import ActorBehaviors
from shared.models.controller import ProcessStates
from shared.models.messages import Message


class State:
    """Actor state is intentionally ephemeral and only in-memory for the lifespan of the
    actor container"""

    def __init__(self, message: Message) -> None:
        self.key = message.metadata.actor_behavior
        self._cache: dict[ActorBehaviors, object] = {}

    def _set_cache(self, dto: object) -> None:
        self._cache[self.key] = dto

    def get_cache(self) -> object | None:
        return self._cache.get(self.key)

    def set_controller_process(self, dto: ProcessStates) -> None:
        self._set_cache(dto)
