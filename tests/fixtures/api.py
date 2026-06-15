# pylint: disable=duplicate-code
import asyncio
from contextlib import asynccontextmanager
from pytest import fixture
from fastapi import FastAPI, Request
from actors.handler import Handler
from actors.mailbox import Mailbox
from actors.static_data.read import Read
from api.v1.helpers.load_executable import load_executable
from shared.log.helpers.api_log_serializer import LogSerializer
from shared.log.writer import Writer
from shared.log.helpers.error import Error
from shared.log.helpers.core import build as core_log
from shared.models.constants import Events, LogLevel
from shared.models.side_effects import MailboxSideEffects, HandlerSideEffects
from shared.models.constants import StaticDataNames


@asynccontextmanager
async def _app_state(config_log, config_api):
    app = FastAPI()
    s = app.state
    s.log = Writer(config_log)
    s.log_error_helper = Error()
    s.format_log = LogSerializer()
    s.config_log = config_log
    s.app_version = config_api.AppVersion
    s.log.write_core(
        core_log(config_log, LogLevel.INFO, Events.STARTUP, "Startup complete")
    )
    app.state.mailbox = Mailbox(MailboxSideEffects(queue=asyncio.Queue()))
    app.state.ready_mailbox = Mailbox(MailboxSideEffects(queue=asyncio.Queue()))
    handler_side_effects = HandlerSideEffects(
        mailbox=app.state.mailbox,
        ready_mailbox=app.state.ready_mailbox,
        static_data=Read(StaticDataNames.HANDLER),
        create_task=asyncio.create_task,
        load_executable=load_executable,
    )
    app.state.handler = Handler(handler_side_effects)
    app.state.handler_task = app.state.handler.start()
    try:
        yield
    finally:
        app.state.handler_task.cancel()
        try:
            await app.state.handler_task
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
