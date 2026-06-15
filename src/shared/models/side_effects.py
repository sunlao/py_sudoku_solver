from asyncio import Queue, Task
from collections.abc import Callable, Coroutine
from typing import Any
from pydantic import BaseModel
from actors.static_data.read import Read
from shared.models.messages import MessageReceive
from shared.models.policy import DTO_EDGE_CONFIG



class MailboxSideEffects(BaseModel):
    """DTO for mailbox construction"""

    model_config = DTO_EDGE_CONFIG

    queue: Queue[MessageReceive ]

class HandlerSideEffects(BaseModel):
    """DTO for handler side-effect dependencies"""

    model_config = DTO_EDGE_CONFIG

    mailbox: Any
    ready_mailbox: Any | None
    static_data: Read
    create_task: Callable[[Coroutine[Any, Any, None]], Task[None]]
    load_executable: Callable[[str], Callable]
