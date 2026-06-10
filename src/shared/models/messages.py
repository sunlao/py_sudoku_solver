from datetime import datetime
from typing import Generic
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
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


# fmt: off
class Board(BaseModel):
    """Sudoku board containing exactly 81 cells"""

    model_config = DTO_CONFIG
    cells: tuple[
        Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell,
        Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell,
        Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell,
        Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell,
        Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell,
        Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell,
        Cell, Cell, Cell,
    ]
    @field_validator("cells")
    @classmethod
    def validate_unique_coordinates(cls, cells: tuple[Cell, ...]) -> tuple[Cell, ...]:
        results = {(c.row, c.column) for c in cells}
        if len(results) != 81:
            raise ValueError(
                "Board must contain exactly one cell for every row/column coordinate"
            )
        return cells


class Startup(BaseModel):
    """Content DTO for startup messages"""

    model_config = DTO_CONFIG
    board: Board


class Message(BaseModel, Generic[INPUTTYPE]):
    """Generic message DTO composed of metadata and typed content"""

    model_config = DTO_CONFIG
    metadata: Metadata
    content: INPUTTYPE
