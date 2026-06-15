import asyncio
from fastapi import APIRouter, Request, Response, status
from api.v1.helpers.client import client
from shared.models.api import ReadyResponse
from shared.models.constants import MessageTypes
from shared.models.messages import MessageRecieve, Metadata, Ready

router = APIRouter()


@router.get("/ready", response_model=ReadyResponse)
async def ready(request: Request, response: Response) -> ReadyResponse:
    mailbox = request.app.state.mailbox
    ready_mailbox = request.app.state.ready_mailbox
    handler_task = request.app.state.handler_task
    check_mailbox = mailbox is not None
    check_ready_mailbox = ready_mailbox is not None
    check_handler = not handler_task.done() and not handler_task.cancelled()
    handler_result = False
    if check_mailbox and check_ready_mailbox and check_handler:
        probe = MessageRecieve(
            metadata=Metadata(message_type=MessageTypes.READY), client=client, content=Ready()
        )
        await mailbox.enqueue(probe)
        try:
            ack = await asyncio.wait_for(ready_mailbox.dequeue(), timeout=1)
            handler_result = ack.metadata.message_id == probe.metadata.message_id
        except asyncio.TimeoutError:
            handler_result = False
    api_ready = (
        check_mailbox and check_ready_mailbox and check_handler and handler_result
    )
    if not api_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadyResponse(
        API=api_ready,
        Mailbox=check_mailbox and check_ready_mailbox,
        Handler=handler_result,
    )
