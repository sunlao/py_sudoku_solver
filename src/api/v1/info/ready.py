from fastapi import APIRouter, Request, Response, status
from shared.models.api import ReadyResponse
from shared.models.constants import ActorBehaviors
from shared.models.messages import Message, Metadata, Ready

router = APIRouter()


@router.get("/ready", response_model=ReadyResponse)
async def ready(request: Request, response: Response) -> ReadyResponse:
    mailbox = request.app.state.mailbox
    test_mailbox = request.app.state.test_mailbox
    handler_task = request.app.state.handler_task
    check_mailbox = mailbox is not None
    check_test_mailbox = test_mailbox is not None
    check_handler = not handler_task.done() and not handler_task.cancelled()
    handler_result = False
    api_ready = False
    if check_mailbox and check_test_mailbox and check_handler:
        api_ready = True
        probe = Message(
            metadata=Metadata(actor_behavior=ActorBehaviors.TEST_READY),
            content=Ready(),
        )
        # shared mailbox/handler at the FastAPI level for all actors
        await mailbox.enqueue(probe)
        try:
            # shared test mailox the shared handler uses to route tests ressponses
            ack = await request.app.state.wait(test_mailbox.dequeue(), timeout=5)
            handler_result = ack.metadata.message_id == probe.metadata.message_id
        except request.app.state.time_out:
            handler_result = False
    error = check_mailbox and check_test_mailbox and check_handler and handler_result
    if not error:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadyResponse(
        API=api_ready,
        Mailbox=check_mailbox and check_test_mailbox,
        Handler=handler_result,
    )
