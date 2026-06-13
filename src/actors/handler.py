from collections.abc import Callable
from importlib import import_module
import asyncio
from shared.models.messages import Message
from actors.mailbox import Mailbox
from actors.static_data.read import Read


class Handler:
    """Handler dequeues, routes and sends telemetry"""

    def __init__(self, mailbox: Mailbox, test: Mailbox | None = None) -> None:
        self.mailbox = mailbox
        self.test = test
        self.static_data = Read("handler")

    def _executable(self, route: str) -> Callable:
        module_path, class_name, method_name = route.rsplit(".", 2)
        cls = getattr(import_module(module_path), class_name)
        return getattr(cls(), method_name)

    async def _process_loop(self) -> None:
        while True:
            message = await self.mailbox.dequeue()
            await self._route(message)

    async def _route(self, message: Message) -> None:
        if self.test is not None:
            await self.test.enqueue(message)
        data = self.static_data.get_handler(message.metadata.message_type)
        executable = self._executable(data.route)
        executable(message)

    def start(self) -> asyncio.Task:
        return asyncio.create_task(self._process_loop())
