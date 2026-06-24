# pylint: disable=duplicate-code
import asyncio
from contextlib import asynccontextmanager
from pytest import fixture
from fastapi import FastAPI, Request
from httpx import AsyncClient
from actors.handler import Handler
from actors.mailbox import Mailbox
from actors.static_data.read import Read
from actors.state import State
from api.v1.helpers.client import transport_client
from api.v1.helpers.load_executable import load_executable
from shared.log.helpers.api_log_serializer import LogSerializer
from shared.log.helpers.error import Error
from shared.log.helpers.core import build as core_log
from shared.log.writer import Writer
from shared.models.constants import Events, LogLevel
from shared.models.side_effects import MailboxSideEffects, HandlerSideEffects


@asynccontextmanager
async def _app_state(config_log, config_api):
    app = FastAPI()
    s = app.state
    s.log = Writer(config_log)
    s.log_error_helper = Error()
    s.format_log = LogSerializer()
    s.wait = asyncio.wait_for
    s.time_out = asyncio.TimeoutError
    s.async_client = AsyncClient
    s.config_log = config_log
    s.app_version = config_api.app_version
    s.log.write_core(
        core_log(config_log, LogLevel.INFO, Events.STARTUP, "Startup complete")
    )
    s.actor_state = State()
    s.mailbox = Mailbox(MailboxSideEffects(queue=asyncio.Queue()))
    s.test_mailbox = Mailbox(MailboxSideEffects(queue=asyncio.Queue()))
    s.transport_client = transport_client
    handler_side_effects = HandlerSideEffects(
        mailbox=s.mailbox,
        test_mailbox=s.test_mailbox,
        static_data=Read,
        create_task=asyncio.create_task,
        load_executable=load_executable,
        transport_client=s.transport_client,
        fastapi_app=app,
        gather=asyncio.gather,
        state=s.actor_state,
    )
    s.handler = Handler(handler_side_effects)
    s.handler_task = s.handler.start()
    try:
        yield app
    finally:
        s.handler_task.cancel()
        try:
            await s.handler_task
        except asyncio.CancelledError:
            pass

        s.log.write_core(
            core_log(config_log, LogLevel.INFO, Events.SHUTDOWN, "Shutdown complete")
        )


@fixture(name="api_with_state")
async def f_api_with_state(config_log, config_api):
    async with _app_state(config_log, config_api) as app:
        yield app


@fixture
async def api_request(api_with_state: FastAPI) -> Request:
    scope = {
        "type": "http",
        "app": api_with_state,
        "headers": [],
        "method": "GET",
        "path": "/_test",
        "query_string": b"",
    }
    return Request(scope)
