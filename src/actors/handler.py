from shared.models.constants import MessageType
from shared.models.messages import Message, ActorBehaviors
from shared.models.side_effects import HandlerSideEffects, ActorSideEffects


class Handler:
    """Handler dequeues, routes and sends telemetry"""

    def __init__(self, dto: HandlerSideEffects) -> None:
        """Instantiate side effects from FastAPI on startup"""
        self.mailbox = dto.mailbox
        self.test_mailbox = dto.test_mailbox
        self.create_task = dto.create_task
        self.load_executable = dto.load_executable
        self.actor_side_effects = ActorSideEffects(
            static_data=dto.static_data,
            transport_client=dto.transport_client,
            fastapi_app=dto.fastapi_app,
            gather=dto.gather,
        )

    def _executable(self, route: str):
        return self.load_executable(route)

    @staticmethod
    def _route_name(actor_behavior: ActorBehaviors) -> str:
        a, b = actor_behavior.split(".", maxsplit=1)
        actor = a.replace("-", "_")
        behavior = b.replace("-", "_")
        behavior_title = behavior.title().replace("_", "")
        return f"actors.actor_tasks.{actor}.{behavior}.{behavior_title}.director"

    async def _process_loop(self) -> None:
        while True:
            message = await self.mailbox.dequeue()
            await self._route(message)

    async def _route(self, dto: Message) -> None:
        if dto.metadata.type == MessageType.TEST:
            await self.test_mailbox.enqueue(dto)
            return
        route_name = self._route_name(dto.metadata.actor_behavior)
        executable = self._executable(route_name)
        await executable(self.actor_side_effects, dto)

    def start(self):
        return self.create_task(self._process_loop())
