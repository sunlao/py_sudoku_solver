import asyncio
from shared.models.messages import Message


class Mailbox:
    """FIFO async mailbox for actor messages"""

    def __init__(self) -> None:
        self._queue: asyncio.Queue[Message] = asyncio.Queue()

    async def enqueue(self, message: Message) -> None:
        """Put a message on the queue"""
        await self._queue.put(message)

    async def dequeue(self) -> Message:
        """Get a message from the queue (blocks if empty)"""
        return await self._queue.get()
