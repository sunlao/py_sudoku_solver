from fastapi import APIRouter, Request, status
from shared.models.messages import Message

router = APIRouter()


@router.post("/start/", response_model=None, status_code=status.HTTP_202_ACCEPTED)
async def start_up(request: Request, dto: Message) -> None:
    print(f"\nstart: {dto.metadata.actor_behavior}\n")
