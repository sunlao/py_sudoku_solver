from fastapi import APIRouter, Request, status
from shared.models.messages import Message, Startup

router = APIRouter()


@router.post("/start-up", response_model=None, status_code=status.HTTP_202_ACCEPTED)
async def start_up(request: Request, dto: Message[Startup]) -> None:
    print(f"\nstart-up: {dto.metadata.actor_behavior}")
    mailbox = request.app.state.mailbox
    await mailbox.enqueue(dto)
