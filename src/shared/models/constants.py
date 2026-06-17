from enum import StrEnum
from typing import NamedTuple


class ActorNames(StrEnum):
    CONTROLLER = "controller"
    GAME = "game"
    BOARD = "board"
    ROW1 = "row1"
    ROW2 = "row2"
    ROW3 = "row3"
    ROW4 = "row4"
    ROW5 = "row5"
    ROW6 = "row6"
    ROW7 = "row7"
    ROW8 = "row8"
    ROW9 = "row9"
    BOX1 = "box1"
    BOX2 = "box2"
    BOX3 = "box3"
    BOX4 = "box4"
    BOX5 = "box5"
    BOX6 = "box6"
    BOX7 = "box7"
    BOX8 = "box8"
    BOX9 = "box9"
    COLUMN1 = "column1"
    COLUMN2 = "column2"
    COLUMN3 = "column3"
    COLUMN4 = "column4"
    COLUMN5 = "column5"
    COLUMN6 = "column6"
    COLUMN7 = "column7"
    COLUMN8 = "column8"
    COLUMN9 = "column9"


class ActorBehaviors(StrEnum):
    """Constants for supported actor behaviors."""

    CONTROLLER_START_UP = "controller.start-up"
    TEST_TEST = "test.test"


class Audit(NamedTuple):
    last_hash: str | None


class DebugStatus(StrEnum):
    OK = "ok"
    ERROR = "error"


class Environments(StrEnum):
    """Constants for Supported Environments"""

    DEV = "dev"
    CI = "ci"


class Events(StrEnum):
    """Supported Events"""

    STARTUP = "startup"
    SHUTDOWN = "shutdown"
    ACCESS = "access"
    HTTP_ERROR = "http_error"
    DBOPEN = "db_open"
    POOLSNAPSHOT = "pool_snap_shot"
    JOB = "job"
    QUIESCE = "quiesce"


# Starlette/Uvicorn insist on lower case
class LogLevel(StrEnum):
    """Log Levels formatted for Starlette/Uvicorn"""

    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


# Starlette/Uvicorn insist on lower case
class PathParts(StrEnum):
    """DTO to Support Tracing Errors. Trace Event paths are filtered and trimmed by
    path parts"""

    SRC = "src"
    TESTS = "tests"


class Services(StrEnum):
    """Pythonic Sudoku Solver Services"""

    API = "pss-api"


class StaticDataNames(StrEnum):
    CONTROLLER = "controller"
    HANDLER = "handler"


class ProcessStatuses(StrEnum):
    STARTED = "started"
    IDLE = "idle"
