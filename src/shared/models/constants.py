from enum import StrEnum
from typing import NamedTuple


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


class MessageTypes(StrEnum):
    """Constants for Supported Environments"""

    STARTUP = "start-up"


# Starlette/Uvicorn insist on lower case
class PathParts(StrEnum):
    """DTO to Support Tracing Errors. Trace Event paths are filtered and trimmed by
    path parts"""

    SRC = "src"
    TESTS = "tests"


class Services(StrEnum):
    """Pythonic Sudoku Solver Services"""

    API = "pss-api"
