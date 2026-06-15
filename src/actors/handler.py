from actors.static_data.read import HandlerInput
from shared.models.messages import Message, MessageTypes
from shared.models.side_effects import HandlerSideEffects


class Handler:
    """Handler dequeues, routes and sends telemetry"""

    def __init__(self, dto: HandlerSideEffects) -> None:
        self.mailbox = dto.mailbox
        self.test_mailbox = dto.test_mailbox
        self.static_data = dto.static_data
        self.create_task = dto.create_task
        self.load_executable = dto.load_executable

    def _executable(self, route: str):
        return self.load_executable(route)

    async def _process_loop(self) -> None:
        while True:
            message = await self.mailbox.dequeue()
            await self._route(message)

    async def _route(self, message: Message) -> None:
        if self.test_mailbox is not None:
            await self.test_mailbox.enqueue(message)
        # support api info ready
        if message.metadata.message_type == MessageTypes.READY:
            return
        dto = HandlerInput(name=message.metadata.message_type)
        data = self.static_data.handler(dto)
        executable = self._executable(data.route)
        executable(message)

    def start(self):
        return self.create_task(self._process_loop())
