# pylint: disable=duplicate-code
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from httpx import AsyncClient
from starlette.responses import PlainTextResponse
from actors.handler import Handler
from actors.mailbox import Mailbox
from actors.static_data.read import Read
from api.metadata import tags
from api.v1.addresses import controller, game
from api.v1.helpers.boards import Boards
from api.v1.helpers.client import transport_client
from api.v1.helpers.messages import start_up
from api.v1.helpers.load_executable import load_executable
from api.v1.info import ready, version
from shared.config.locker import Locker
from shared.log.helpers.api_log_serializer import LogSerializer
from shared.log.helpers.core import build as core_log
from shared.log.helpers.error import Error
from shared.log.writer import Writer
from shared.models.api import ASGIEvent, RootResponse
from shared.models.constants import Events, LogLevel, ActorNames
from shared.models.log import EventError
from shared.models.side_effects import MailboxSideEffects, HandlerSideEffects

locker = Locker()
config_log = locker.log()
api_log = locker.api()
start_up_message = start_up(Boards().start_up())


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.log = Writer(config_log)
    app.state.log_error_helper = Error()
    app.state.format_log = LogSerializer()
    app.state.wait = asyncio.wait_for
    app.state.time_out = asyncio.TimeoutError
    app.state.async_client = AsyncClient
    app.state.config_log = config_log
    app.state.app_version = api_log.app_version
    # Start mailboxes
    app.state.mailbox = Mailbox(MailboxSideEffects(queue=asyncio.Queue()))
    app.state.test_mailbox = Mailbox(MailboxSideEffects(queue=asyncio.Queue()))
    handler_side_effects = HandlerSideEffects(
        mailbox=app.state.mailbox,
        test_mailbox=app.state.test_mailbox,
        static_data=Read,
        create_task=asyncio.create_task,
        load_executable=load_executable,
    )
    app.state.handler = Handler(handler_side_effects)
    app.state.handler_task = app.state.handler.start()
    app.state.transport_client = transport_client(app)
    async with app.state.transport_client(app) as client_api:
        await client_api.post(
            f"/address/{ActorNames.CONTROLLER}/start-up",
            json=start_up_message.model_dump(mode="json"),
        )
    msg = "API Service Startup complete"
    core = core_log(config_log, LogLevel.INFO, Events.STARTUP, msg)
    app.state.log.write_core(core)
    try:
        yield
    finally:
        app.state.handler_task.cancel()
        try:
            await app.state.handler_task
        except asyncio.CancelledError:
            pass
        msg = "API Service Shutdown complete"
        core = core_log(config_log, LogLevel.INFO, Events.SHUTDOWN, msg)
        app.state.log.write_core(core)


def create_api() -> FastAPI:
    _api = FastAPI(
        title="Actor API Service",
        version=f"Version: {api_log.app_version}",
        openapi_tags=tags(),
        lifespan=lifespan,
    )

    # used for central api logging events
    @_api.middleware("http")
    async def _access_mw(
        request: Request, call_next
    ):  # pylint: disable=too-many-locals
        start = config_log.TimeCounter()
        request.app.state.txid = request.app.state.format_log.transaction_id(request)
        try:
            response: Response = await call_next(request)
            error = None
            trace_back_nfo = None
        except Exception as e:  # pylint: disable=broad-except
            response = PlainTextResponse(
                "Unknown Internal Server Error", status_code=500
            )
            error = e
            trace_back_nfo = request.app.state.log_error_helper.trace_back_nfo(e)
        finally:
            duration = int((config_log.TimeCounter() - start) * 1000)
            msg = request.app.state.format_log.message(response)
            core_event = core_log(config_log, LogLevel.INFO, Events.ACCESS, msg)
            event_input = ASGIEvent(
                Request=request, Response=response, DurationMS=duration
            )
            log_dto = request.app.state.format_log.build(core_event, event_input)
            if error is None:
                request.app.state.log.write_event(dto=log_dto)
            else:
                err_core = core_log(
                    config_log, LogLevel.ERROR, Events.HTTP_ERROR, str(error)
                )
                error_event_input = ASGIEvent(
                    Request=request, Response=response, DurationMS=duration
                )
                error_event_dto = request.app.state.format_log.build(
                    err_core, error_event_input
                )
                error_event_error_dto = EventError(
                    Core=error_event_dto.Core,
                    Event=error_event_dto.Event,
                    Error=trace_back_nfo,
                )
                request.app.state.log.write_event_error(dto=error_event_error_dto)
        return response

    @_api.get("/api/v1")
    async def root() -> RootResponse:
        """Application Root"""
        return RootResponse(Message="Sudoku Solver API Service is up!")

    # routing
    _api.include_router(version.router, prefix="/api/v1/info", tags=["info"])
    _api.include_router(ready.router, prefix="/api/v1/info", tags=["info"])
    _api.include_router(
        controller.router, prefix="/address/controller", tags=["actor", "controller"]
    )
    _api.include_router(game.router, prefix="/address/game", tags=["actor", "game"])

    return _api


api = create_api()
