from fastapi import APIRouter, Request, status, HTTPException
from shared.models.messages import Message, RBCCells

router = APIRouter()


@router.post("/eval/", response_model=None, status_code=status.HTTP_202_ACCEPTED)
async def start_up(request: Request, dto: Message[RBCCells]) -> None:
    mailbox = request.app.state.mailbox
    try:
        await mailbox.enqueue(dto)
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Message not accepted",
        ) from exc

