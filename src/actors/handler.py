from actors.static_data.read import HandlerInput
from shared.models.messages import Message, ActorBehaviors
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
        if message.metadata.actor_behavior == ActorBehaviors.TEST_READY:            
            await self.test_mailbox.enqueue(message)
            return
        if message.metadata.actor_behavior == ActorBehaviors.TEST_SEND:            
            await self.test_mailbox.enqueue(message)
        dto = HandlerInput(name=message.metadata.actor_behavior)
        data = self.static_data.handler(dto)
        executable = self._executable(data.route)
        executable(message)

    def start(self):
        return self.create_task(self._process_loop())
