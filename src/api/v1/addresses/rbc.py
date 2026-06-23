from fastapi import APIRouter, status, HTTPException
from shared.models.messages import Message

router = APIRouter()


@router.post("/start/", response_model=None, status_code=status.HTTP_202_ACCEPTED)
async def start_up(dto: Message) -> None:
    try:
        print(f"start: {dto.metadata.actor_behavior}\n")
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Message not accepted",
        ) from exc


@router.post("/cell-update/", response_model=None, status_code=status.HTTP_202_ACCEPTED)
async def cell_update(dto: Message) -> None:
    try:
        print(f"cell-update: {dto.metadata.actor_behavior}\n")
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Message not accepted",
        ) from exc