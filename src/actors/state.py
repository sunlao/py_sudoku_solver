from shared.models.constants import ActorNames
from shared.models.state import ActorDomainStates
from shared.models.messages import Message, Board


class State:
    """Actor state is intentionally ephemeral and only in-memory for the lifespan of the
    actor run time container
      - logically partitioned by actor key associated with message"""

    def __init__(self) -> None:
        self._cache: dict[ActorNames, object] = {}

    def _key(self, message: Message) -> ActorNames:
        a, _ = message.metadata.actor_behavior.split(".", maxsplit=1)
        return ActorNames(a)

    def get_cache(self, message: Message) -> object:
        return self._cache.get(self._key(message))

    def set_game_board(self, message: Message, dto: Board) -> None:
        """Set the board state for the game actor"""
        self._cache[self._key(message)] = dto

    def set_actor_domain_states(self, message: Message, dto: ActorDomainStates) -> None:
        """Set the process state for every eligible domain actor behavior for the
        controller actor"""
        self._cache[self._key(message)] = dto
