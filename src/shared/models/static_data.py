from pydantic import BaseModel, Field
from shared.models.policy import DTO_CONFIG
from shared.models.constants import ActorNames

class Actor(BaseModel):
    model_config = DTO_CONFIG

    name: ActorNames
    addresses: tuple[str, ...]


class Actors(BaseModel):
    model_config = DTO_CONFIG

    actors: tuple[Actor, ...]