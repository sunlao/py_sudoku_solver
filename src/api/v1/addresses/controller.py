from fastapi import APIRouter, Request, status
from shared.models.messages import Message

router = APIRouter()


@router.post("/start-up", response_model=None, status_code=status.HTTP_202_ACCEPTED)
async def ready(request: Request, dto: Message) -> None:
    print(f"\ntype: {dto.metadata.message_type}\n")
