import re
from pydantic import BaseModel

# , field_validator
from shared.models.policy import DTO_CONFIG
from shared.models.constants import ActorNames, BehaviorNames, CellIds

NAME_FORMAT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class Actor(BaseModel):
    model_config = DTO_CONFIG

    name: ActorNames
    rbc_flag: bool
    domain_flag: bool
    cells: tuple[CellIds, ...] | None = None


class Behavior(BaseModel):
    model_config = DTO_CONFIG

    name: BehaviorNames


class Actors(BaseModel):
    model_config = DTO_CONFIG
    actors: tuple[Actor, ...]
