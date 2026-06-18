from pydantic import BaseModel
from shared.models.policy import DTO_CONFIG
from shared.models.constants import ActorNames, StaticDataNames, ActorBehaviors


class StaticDataInit(BaseModel):
    model_config = DTO_CONFIG

    name: StaticDataNames

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
    """DTO to get handler route static data by actor:behavior"""

    model_config = DTO_CONFIG
    name: ActorBehaviors
