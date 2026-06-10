import asyncio
from shared.models.messages import Message
from actors.mailbox import Mailbox


class Handler:
    """Handler dequeues, routes and sends telemetry"""

    def __init__(self, mailbox: Mailbox, test: Mailbox | None = None) -> None:
        self.mailbox = mailbox
        self.test = test

    async def _process_loop(self) -> None:
        while True:
            message = await self.mailbox.dequeue()
            await self._route(message)

    async def _route(self, message: Message) -> None:
        if self.test is not None:
            await self.test.enqueue(message)

    def start(self) -> asyncio.Task:
        return asyncio.create_task(self._process_loop())
