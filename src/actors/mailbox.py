from shared.models.messages import MessageRecieve
from shared.models.side_effects import MailboxSideEffects


class Mailbox:
    """FIFO async mailbox for actor messages"""

    def __init__(self, dto: MailboxSideEffects) -> None:
        self._queue = dto.queue

    async def enqueue(self, message: MessageRecieve) -> None:
        """Put a message on the queue"""
        await self._queue.put(message)

    async def dequeue(self) -> MessageRecieve:
        """Get a message from the queue (blocks if empty)"""
        return await self._queue.get()
