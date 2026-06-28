from enum import StrEnum
from typing import NamedTuple


class ActorNames(StrEnum):
    """Constants for supported actors"""

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
    CONTROLLER_UPDATE_STATUS = "controller.update-status"

    GAME_START = "game.start"
    GAME_CELL_UPDATE = "game.cell-update"

    BOARD_START = "board.start"
    BOARD_CELL_UPDATE = "board.cell-update"

    ROW1_START = "row1.start"
    ROW1_CELL_UPDATE = "row1.cell-update"
    ROW2_START = "row2.start"
    ROW2_CELL_UPDATE = "row2.cell-update"
    ROW3_START = "row3.start"
    ROW3_CELL_UPDATE = "row3.cell-update"
    ROW4_START = "row4.start"
    ROW4_CELL_UPDATE = "row4.cell-update"
    ROW5_START = "row5.start"
    ROW5_CELL_UPDATE = "row5.cell-update"
    ROW6_START = "row6.start"
    ROW6_CELL_UPDATE = "row6.cell-update"
    ROW7_START = "row7.start"
    ROW7_CELL_UPDATE = "row7.cell-update"
    ROW8_START = "row8.start"
    ROW8_CELL_UPDATE = "row8.cell-update"
    ROW9_START = "row9.start"
    ROW9_CELL_UPDATE = "row9.cell-update"

    BOX1_START = "box1.start"
    BOX1_CELL_UPDATE = "box1.cell-update"
    BOX2_START = "box2.start"
    BOX2_CELL_UPDATE = "box2.cell-update"
    BOX3_START = "box3.start"
    BOX3_CELL_UPDATE = "box3.cell-update"
    BOX4_START = "box4.start"
    BOX4_CELL_UPDATE = "box4.cell-update"
    BOX5_START = "box5.start"
    BOX5_CELL_UPDATE = "box5.cell-update"
    BOX6_START = "box6.start"
    BOX6_CELL_UPDATE = "box6.cell-update"
    BOX7_START = "box7.start"
    BOX7_CELL_UPDATE = "box7.cell-update"
    BOX8_START = "box8.start"
    BOX8_CELL_UPDATE = "box8.cell-update"
    BOX9_START = "box9.start"
    BOX9_CELL_UPDATE = "box9.cell-update"

    COLUMN1_START = "column1.start"
    COLUMN1_CELL_UPDATE = "column1.cell-update"
    COLUMN2_START = "column2.start"
    COLUMN2_CELL_UPDATE = "column2.cell-update"
    COLUMN3_START = "column3.start"
    COLUMN3_CELL_UPDATE = "column3.cell-update"
    COLUMN4_START = "column4.start"
    COLUMN4_CELL_UPDATE = "column4.cell-update"
    COLUMN5_START = "column5.start"
    COLUMN5_CELL_UPDATE = "column5.cell-update"
    COLUMN6_START = "column6.start"
    COLUMN6_CELL_UPDATE = "column6.cell-update"
    COLUMN7_START = "column7.start"
    COLUMN7_CELL_UPDATE = "column7.cell-update"
    COLUMN8_START = "column8.start"
    COLUMN8_CELL_UPDATE = "column8.cell-update"
    COLUMN9_START = "column9.start"
    COLUMN9_CELL_UPDATE = "column9.cell-update"

    TEST_BAD = "test.bad"
    TEST_READY = "test.ready"


class Audit(NamedTuple):
    last_hash: str | None


class CellIds(StrEnum):
    R1C1 = "r1c1"
    R1C2 = "r1c2"
    R1C3 = "r1c3"
    R1C4 = "r1c4"
    R1C5 = "r1c5"
    R1C6 = "r1c6"
    R1C7 = "r1c7"
    R1C8 = "r1c8"
    R1C9 = "r1c9"

    R2C1 = "r2c1"
    R2C2 = "r2c2"
    R2C3 = "r2c3"
    R2C4 = "r2c4"
    R2C5 = "r2c5"
    R2C6 = "r2c6"
    R2C7 = "r2c7"
    R2C8 = "r2c8"
    R2C9 = "r2c9"

    R3C1 = "r3c1"
    R3C2 = "r3c2"
    R3C3 = "r3c3"
    R3C4 = "r3c4"
    R3C5 = "r3c5"
    R3C6 = "r3c6"
    R3C7 = "r3c7"
    R3C8 = "r3c8"
    R3C9 = "r3c9"

    R4C1 = "r4c1"
    R4C2 = "r4c2"
    R4C3 = "r4c3"
    R4C4 = "r4c4"
    R4C5 = "r4c5"
    R4C6 = "r4c6"
    R4C7 = "r4c7"
    R4C8 = "r4c8"
    R4C9 = "r4c9"

    R5C1 = "r5c1"
    R5C2 = "r5c2"
    R5C3 = "r5c3"
    R5C4 = "r5c4"
    R5C5 = "r5c5"
    R5C6 = "r5c6"
    R5C7 = "r5c7"
    R5C8 = "r5c8"
    R5C9 = "r5c9"

    R6C1 = "r6c1"
    R6C2 = "r6c2"
    R6C3 = "r6c3"
    R6C4 = "r6c4"
    R6C5 = "r6c5"
    R6C6 = "r6c6"
    R6C7 = "r6c7"
    R6C8 = "r6c8"
    R6C9 = "r6c9"

    R7C1 = "r7c1"
    R7C2 = "r7c2"
    R7C3 = "r7c3"
    R7C4 = "r7c4"
    R7C5 = "r7c5"
    R7C6 = "r7c6"
    R7C7 = "r7c7"
    R7C8 = "r7c8"
    R7C9 = "r7c9"

    R8C1 = "r8c1"
    R8C2 = "r8c2"
    R8C3 = "r8c3"
    R8C4 = "r8c4"
    R8C5 = "r8c5"
    R8C6 = "r8c6"
    R8C7 = "r8c7"
    R8C8 = "r8c8"
    R8C9 = "r8c9"

    R9C1 = "r9c1"
    R9C2 = "r9c2"
    R9C3 = "r9c3"
    R9C4 = "r9c4"
    R9C5 = "r9c5"
    R9C6 = "r9c6"
    R9C7 = "r9c7"
    R9C8 = "r9c8"
    R9C9 = "r9c9"


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


class MessageType(StrEnum):
    """Type defining messages"""

    DOMAIN = "domain"
    ADMIN = "admin"
    TEST = "test"


# Starlette/Uvicorn insist on lower case
class PathParts(StrEnum):
    """DTO to Support Tracing Errors. Trace Event paths are filtered and trimmed by
    path parts"""

    SRC = "src"
    TESTS = "tests"


class Services(StrEnum):
    """Pythonic Sudoku Solver Services"""

    API = "pss-api"
    TEST = "pss-test"


class ActorDomainStatus(StrEnum):
    IDLE = "idle"
    STARTED = "started"
    WORKING = "working"
