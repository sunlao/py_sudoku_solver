from datetime import datetime
from typing import Generic
from uuid import UUID
from pydantic import BaseModel, Field
from shared.models.constants import MessageTypes
from shared.models.policy import DTO_CONFIG, INPUTTYPE


class Metadata(BaseModel):
    """Metadata wrapper for all messages"""

    model_config = DTO_CONFIG
    message_id: UUID = Field(..., description="Unique message identifier")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Message creation time"
    )
    message_type: MessageTypes = Field(..., description="Type of message content")


class Cell(BaseModel):
    """Single cell in sudoku board"""

    model_config = DTO_CONFIG
    row: int = Field(ge=1, le=9)
    column: int = Field(ge=1, le=9)
    box: int = Field(ge=1, le=9)
    value: int | None = Field(default=None, ge=1, le=9)


class Row(BaseModel):
    """Row of 9 cells"""

    model_config = DTO_CONFIG
    cells: tuple[Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell]


class Board(BaseModel):
    """9x9 sudoku board"""

    model_config = DTO_CONFIG
    rows: tuple[Row, Row, Row, Row, Row, Row, Row, Row, Row]


class Startup(BaseModel):
    """Content DTO for startup messages"""

    model_config = DTO_CONFIG
    board: Board


class Message(BaseModel, Generic[INPUTTYPE]):
    """Generic message DTO composed of metadata and typed content"""

    model_config = DTO_CONFIG
    metadata: Metadata
    content: INPUTTYPE
