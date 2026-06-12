from pydantic import BaseModel, Field
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
