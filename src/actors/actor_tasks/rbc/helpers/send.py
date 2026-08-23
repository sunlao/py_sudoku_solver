from fastapi import status
from uuid import UUID
from shared.models.constants import ActorBehaviors
from shared.models.messages import Cell, Message, Metadata, RBCCells
from shared.models.side_effects import ActorSideEffects


class Send:

    @staticmethod
    def _check_error(
        status_code: status, actor_behavior: ActorBehaviors, message_id: UUID
    ) -> None:
        if status_code != status.HTTP_202_ACCEPTED:
            msg = f"{actor_behavior} failed to send MessageID: {message_id}"
            raise RuntimeError(msg)

    @staticmethod
    def _msg_game_update(dto: Cell) -> Message[Cell]:
        return Message[Cell](
            metadata=Metadata(actor_behavior=ActorBehaviors.GAME_CELL_UPDATE),
            content=dto,
        )

    @staticmethod
    def _msg_rbc_evaluate(dto: RBCCells) -> Message[RBCCells]:
        return Message[RBCCells](
            metadata=Metadata(
                actor_behavior=ActorBehaviors(f"{dto.actor}.evaluate"),
                rbc_flag=True,
            ),
            content=dto,
        )

    async def send_game_update(
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

    async def send_rbc_evaluate(
        self, side_effects: ActorSideEffects, rbc_cells: RBCCells
    ) -> None:
        dto = self._msg_rbc_evaluate(rbc_cells)
        async with side_effects.transport_client(
            side_effects.fastapi_app, dto
        ) as client:
            response = await client.post("/", json=dto.model_dump(mode="json"))
            self._check_error(
                response.status_code,
                dto.metadata.actor_behavior,
                dto.metadata.message_id,
            )
