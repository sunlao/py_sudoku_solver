import re
from pydantic import BaseModel, field_validator
from shared.models.policy import DTO_CONFIG
from shared.models.constants import ActorNames, BehaviorNames

NAME_FORMAT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class Actor(BaseModel):
    model_config = DTO_CONFIG

    name: ActorNames
    rbc_flag: bool
    process_flag: bool
    behaviors: tuple[BehaviorNames, ...]

    # @field_validator("name")
    # @classmethod
    # def validate_name(cls, value: str) -> ActorNames:
    #     if not NAME_FORMAT.fullmatch(value):
    #         raise ValueError(f"Invalid actor name: {value}")
    #     return value


class Behavior(BaseModel):
    model_config = DTO_CONFIG

    name: BehaviorNames

    # @field_validator("name")
    # @classmethod
    # def validate_name(cls, value: str) -> BehaviorNames:
    #     if not NAME_FORMAT.fullmatch(value):
    #         raise ValueError(f"Invalid behavior name: {value}")
    #     return value


class Actors(BaseModel):
    model_config = DTO_CONFIG
    actors: tuple[Actor, ...]
