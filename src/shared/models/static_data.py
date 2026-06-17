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


class Route(BaseModel):
    model_config = DTO_CONFIG
    route: str


class RouteName(BaseModel):
    """DTO to get handler static data"""

    model_config = DTO_CONFIG
    name: str
