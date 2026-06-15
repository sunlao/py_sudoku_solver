from datetime import datetime, UTC
from uuid import UUID, uuid4
from typing import Generic
from pydantic import BaseModel, Field, field_validator
from shared.models.constants import Behavior
from shared.models.policy import DTO_CONFIG, INPUTTYPE


class Metadata(BaseModel):
    """Metadata wrapper for all messages"""

    model_config = DTO_CONFIG
    message_id: UUID = Field(default_factory=uuid4)
    times: datetime = Field(default_factory=lambda: datetime.now(UTC))
    message_type: Behavior


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


class Ready(BaseModel):
    """Content DTO for ready probe messages"""

    model_config = DTO_CONFIG


class Message(BaseModel, Generic[INPUTTYPE]):
    """Actor message DTO with async client and content composable by domain"""

    model_config = DTO_CONFIG
    metadata: Metadata
    content: INPUTTYPE
