from fastapi import APIRouter, Request, status
from shared.models.messages import Message, ControllerStartup

router = APIRouter()


@router.post("/start-up/", response_model=None, status_code=status.HTTP_202_ACCEPTED)
async def start_up(request: Request, dto: Message[ControllerStartup]) -> None:
    mailbox = request.app.state.mailbox
    await mailbox.enqueue(dto)
