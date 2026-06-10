import asyncio
from shared.models.messages import Message
from actors.mailbox import Mailbox


class Handler:
    """Handler processes messages from mailbox"""

    def __init__(self, mailbox: Mailbox, test: Mailbox | None = None) -> None:
        self.mailbox = mailbox
        self.test = test
        self.running = False

    async def _process_loop(self) -> None:
        self.running = True
        try:
            while self.running:
                message = await self.mailbox.dequeue()
                await self._route(message)
        except asyncio.CancelledError:
            self.running = False

    async def _route(self, message: Message) -> Message:
        if self.test is not None:
            await self.test.enqueue(message)        

    def start(self) -> asyncio.Task:
        """Start the handler as a background task"""
        return asyncio.create_task(self._process_loop())

    def stop(self) -> None:
        """Stop the handler"""
        self.running = False
