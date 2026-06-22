from shared.models.constants import ActorNames
from shared.models.controller import ProcessStates
from shared.models.messages import Message


class State:
    """Actor state is intentionally ephemeral and only in-memory for the lifespan of the
    actor run time container
      - logically partitioned by actor key associated with message"""

    def __init__(self, message: Message) -> None:
        a, _ = message.metadata.actor_behavior.split(".", maxsplit=1)
        self.key = a
        self._cache: dict[ActorNames, object] = {}

    def _set_cache(self, dto: object) -> None:
        self._cache[self.key] = dto

    def get_cache(self) -> object | None:
        return self._cache.get(self.key)

    def set_controller_process(self, dto: ProcessStates) -> None:
        """Set the process state for every eligible actor behavior for the controller
        actor"""

        self._set_cache(dto)
