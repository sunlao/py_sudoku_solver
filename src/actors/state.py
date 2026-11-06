from shared.models.constants import ActorNames
from shared.models.state import ActorDomainStates
from shared.models.messages import MessageMetadata, Board, RBCCells


class State:
    """Actor state is intentionally ephemeral and only in-memory for the lifespan of the
    actor run time container
      - logically partitioned by actor key associated with message"""

    def __init__(self) -> None:
        self._cache: dict[ActorNames, object] = {}

    def _key(self, message: MessageMetadata) -> ActorNames:
        a, _ = message.metadata.actor_behavior.split(".", maxsplit=1)
        return ActorNames(a)

    def get_cache(self, message: MessageMetadata) -> object:
        return self._cache.get(self._key(message))

    def set_domain_actors_state(
        self, message: MessageMetadata, dto: ActorDomainStates
    ) -> None:
        """Set each of domain actor behavior's process state for the controller"""
        self._cache[self._key(message)] = dto

    def set_game_board(self, message: MessageMetadata, dto: Board) -> None:
        """Set the board state for the game actor"""
        self._cache[self._key(message)] = dto

    def set_rbc_cells(self, message: MessageMetadata, dto: RBCCells) -> None:
        """Reusable code to Set the state for each of the rbc actors"""
        self._cache[self._key(message)] = dto
