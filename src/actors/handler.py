import asyncio
from shared.models.messages import Message
from actors.mailbox import Mailbox


class Handler:
    """Handler processes messages from mailbox"""

    def __init__(self, mailbox: Mailbox) -> None:
        self.mailbox = mailbox
        self.running = False

    async def _process_loop(self) -> None:
        """Continuously dequeue and process messages"""
        self.running = True
        try:
            while self.running:
                message = await self.mailbox.dequeue()
                await self._route(message)
        except asyncio.CancelledError:
            self.running = False

    async def _route(self, message: Message) -> None:
        return message

    def start(self) -> asyncio.Task:
        """Start the handler as a background task"""
        return asyncio.create_task(self._process_loop())

    def stop(self) -> None:
        """Stop the handler"""
        self.running = False
