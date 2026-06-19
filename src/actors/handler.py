from shared.models.messages import Message, ActorBehaviors
from shared.models.side_effects import HandlerSideEffects, ActorSideEffects
from shared.models.static_data import StaticDataInit, RouteName


class Handler:
    """Handler dequeues, routes and sends telemetry"""

    def __init__(self, dto: HandlerSideEffects) -> None:
        """Instantiate side effects from FastAPI on startup"""
        self.mailbox = dto.mailbox
        self.test_mailbox = dto.test_mailbox
        self.create_task = dto.create_task
        static_data_owner = type(self).__name__.lower()
        self.static_data = dto.static_data(StaticDataInit(name=static_data_owner))
        self.load_executable = dto.load_executable
        self.actor_side_effects = ActorSideEffects(
            static_data=dto.static_data, transport_client=dto.transport_client
        )

    def _executable(self, route: str):
        return self.load_executable(route)

    async def _process_loop(self) -> None:
        while True:
            message = await self.mailbox.dequeue()
            await self._route(message)

    async def _route(self, message: Message) -> None:
        if message.metadata.actor_behavior == ActorBehaviors.TEST_READY:
            # Intercept and reoute Ready Message in support of info.ready test api
            await self.test_mailbox.enqueue(message)
            return
        if message.metadata.actor_behavior == ActorBehaviors.TEST_SEND:
            # Intercept and reoute test send Message in support of pytest.
            await self.test_mailbox.enqueue(message)
            return
        route_name = RouteName(name=message.metadata.actor_behavior)
        data = self.static_data.handler_routes(route_name)
        executable = self._executable(data.route)
        executable(self.actor_side_effects, message)

    def start(self):
        return self.create_task(self._process_loop())
