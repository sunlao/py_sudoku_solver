from asyncio import Queue, Task
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from actors.static_data.read import Read
from actors.state import State
from shared.models.messages import Message
from shared.models.policy import DTO_EDGE_CONFIG


class ActorSideEffects(BaseModel):
    """DTO for actor side-effect dependencies
    - Read yml configs as static data
    """

    model_config = DTO_EDGE_CONFIG

    static_data: Callable[[Message], Read]
    transport_client: Callable
    fastapi_app: FastAPI
    gather: Callable[..., Awaitable[tuple[Any, ...]]]
    state: State


class MailboxSideEffects(BaseModel):
    """DTO for mailbox construction
    - asyncio queue"""

    model_config = DTO_EDGE_CONFIG

    queue: Queue[Message]


class HandlerSideEffects(BaseModel):
    """DTO for handler side-effect dependencies
    - mail box
    - test mail box
    - execute async tasks
    - read yml configs as static data
    - transportclient to send messages
    - fast api app
    - asyncio gather
    - actor state
    """

    model_config = DTO_EDGE_CONFIG

    mailbox: Any
    test_mailbox: Any | None
    static_data: Callable[[Message], Read]
    create_task: Callable[[Coroutine[Any, Any, None]], Task[None]]
    load_executable: Callable[[str], Callable]
    transport_client: Callable
    fastapi_app: FastAPI
    gather: Callable[..., Awaitable[tuple[Any, ...]]]
    state: State
