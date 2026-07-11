from pydantic import BaseModel, Field
from shared.models.policy import DTO_CONFIG
from shared.models.constants import CellIds
from shared.models.messages import ActorBehaviors


class RowInput(BaseModel):
    model_config = DTO_CONFIG

    values: tuple[int | None, ...] = Field(min_length=9, max_length=9)


class BoardInput(BaseModel):
    model_config = DTO_CONFIG

    rows: tuple[RowInput, ...] = Field(min_length=9, max_length=9)


class CellBehaviors(BaseModel):
    model_config = DTO_CONFIG

    id: CellIds
    behaviors: tuple[ActorBehaviors, ...]


class CellBehaviorMaps(BaseModel):
    model_config = DTO_CONFIG

    maps: tuple[CellBehaviors, ...]
