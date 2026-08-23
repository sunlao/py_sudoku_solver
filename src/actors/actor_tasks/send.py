from uuid import UUID
from fastapi import status
from shared.models.constants import ActorBehaviors
from shared.models.messages import (
    Board,
    Cell,
    GameStart,
    Message,
    Metadata,
    RBCCells,
)
from shared.models.side_effects import ActorSideEffects, PostControllerUpdate
from shared.models.state import ActorDomainState
from shared.models.static_data import Actor


class Send:

    @staticmethod
    def _check_error(
        status_code: status, actor_behavior: ActorBehaviors, message_id: UUID
    ) -> None:
        if status_code != status.HTTP_202_ACCEPTED:
            msg = f"{actor_behavior} failed to send MessageID: {message_id}"
            raise RuntimeError(msg)

    @staticmethod
    def _msg_controller_update(dto: PostControllerUpdate) -> Message[ActorDomainState]:
        """Build controller ActorDomainState update message"""
        metadata = Metadata(actor_behavior=ActorBehaviors.CONTROLLER_UPDATE_STATUS)
        content = ActorDomainState(
            actor=dto.sending_actor,
            status=dto.sending_status,
            last_director_timestamp=dto.last_director_timestamp,
            rbc_flag=dto.rbc_flag,
        )
        return Message[ActorDomainState](metadata=metadata, content=content)

    @staticmethod
    def _msg_game_start(dto: Board) -> Message[GameStart]:
        m = Metadata(actor_behavior=ActorBehaviors.GAME_START)
        return Message(metadata=m, content=GameStart(board=dto))

    @staticmethod
    def _msg_game_update(dto: Cell) -> Message[Cell]:
        m = Metadata(actor_behavior=ActorBehaviors.GAME_CELL_UPDATE)
        return Message[Cell](metadata=m, content=dto)

    @staticmethod
    def msg_rbc_evaluate_board(dto: Board, actor: Actor) -> Message[RBCCells]:
        name = actor.name
        actor_behavior = ActorBehaviors(f"{name}.evaluate")
        meta_data = Metadata(actor_behavior=actor_behavior, rbc_flag=True)
        ids = set(actor.cell_ids)
        cells = tuple(c for c in dto.cells if c.id in ids)
        return Message(metadata=meta_data, content=RBCCells(actor=name, cells=cells))

    async def post_controller_update(self, dto: PostControllerUpdate) -> None:
        """post ActorDomainState update message to a dynamicaly generated route from dto.metadata.actor_behavior
        - /address/v1/{actor}/{behavior}
        """
        msg_dto = self._msg_controller_update(dto)
        async with dto.side_effects.transport_client(
            dto.side_effects.fastapi_app, msg_dto
        ) as client:
            response = await client.post("/", json=msg_dto.model_dump(mode="json"))
            self._check_error(
                response.status_code,
                msg_dto.metadata.actor_behavior,
                msg_dto.metadata.message_id,
            )

    async def post_game_start(self, side_effects: ActorSideEffects, dto: Board) -> None:
        dto = self._msg_game_start(dto)
        async with side_effects.transport_client(
            side_effects.fastapi_app, dto
        ) as client_api:
            response = await client_api.post("/", json=dto.model_dump(mode="json"))
            if response.status_code != status.HTTP_202_ACCEPTED:
                raise RuntimeError(
                    f"{dto.metadata.actor_behavior} failed to send "
                    f"MessageID: {dto.metadata.message_id}"
                )

    async def post_game_update(
        self, side_effects: ActorSideEffects, cell: Cell
    ) -> None:
        dto = self._msg_game_update(cell)
        async with side_effects.transport_client(
            side_effects.fastapi_app, dto
        ) as client:
            response = await client.post("/", json=dto.model_dump(mode="json"))
            self._check_error(
                response.status_code,
                dto.metadata.actor_behavior,
                dto.metadata.message_id,
            )

    async def post_rbc_evaluate(
        self, side_effects: ActorSideEffects, dto: Message[RBCCells]
    ) -> None:
        async with side_effects.transport_client(
            side_effects.fastapi_app, dto
        ) as client:
            response = await client.post("/", json=dto.model_dump(mode="json"))
            self._check_error(
                response.status_code,
                dto.metadata.actor_behavior,
                dto.metadata.message_id,
            )
