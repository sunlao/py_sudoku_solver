from fastapi import APIRouter, Request, status
from shared.models.messages import Message

router = APIRouter()


@router.post("/start-up", response_model=None, status_code=status.HTTP_202_ACCEPTED)
async def start_up(request: Request, dto: Message) -> None:
    print(f"\nstart-up: {dto.metadata.actor_behavior}")
    mailbox = request.app.state.mailbox
    await mailbox.enqueue(dto)
    print("**enqueue msg")
    print(f"content: {dto.content.board.cells}")
