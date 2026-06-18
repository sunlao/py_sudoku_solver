from asyncio import Queue, Task
from collections.abc import Callable, Coroutine
from typing import Any
from pydantic import BaseModel
from actors.static_data.read import Read
from shared.models.constants import StaticDataNames
from shared.models.messages import Message
from shared.models.policy import DTO_EDGE_CONFIG
from shared.models.static_data import StaticDataInit


class ActorSideEffects(BaseModel):
    model_config = DTO_EDGE_CONFIG

    static_data: Callable[[StaticDataInit], Read]


class MailboxSideEffects(BaseModel):
    """DTO for mailbox construction"""

    model_config = DTO_EDGE_CONFIG

    queue: Queue[Message]


class HandlerSideEffects(BaseModel):
    """DTO for handler side-effect dependencies"""

    model_config = DTO_EDGE_CONFIG

    mailbox: Any
    test_mailbox: Any | None
    static_data: Callable[[StaticDataNames], Read]
    create_task: Callable[[Coroutine[Any, Any, None]], Task[None]]
    load_executable: Callable[[str], Callable]
