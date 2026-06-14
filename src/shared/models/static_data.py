from pydantic import BaseModel
from shared.models.policy import DTO_CONFIG
from shared.models.constants import ActorNames


class Actor(BaseModel):
    model_config = DTO_CONFIG

    name: ActorNames
    rbc_flag: bool
    addresses: tuple[str, ...]


class Actors(BaseModel):
    model_config = DTO_CONFIG
    actors: tuple[Actor, ...]


class Startup(BaseModel):
    model_config = DTO_CONFIG
    route: str


class HandlerInput(BaseModel):
    """Content DTO for startup messages"""

    model_config = DTO_CONFIG
    name: str
