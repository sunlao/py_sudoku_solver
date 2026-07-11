from pathlib import Path
from yaml import safe_load
from shared.models.messages import Message
from shared.models.static_data import Actors, Actor
from shared.models.board import CellBehaviorMaps, CellBehaviors


class Read:
    """Get static yml data by file name as a Data Transport Object (DTO)"""

    DIR_PATH = Path(__file__).resolve().parent

    def __init__(self, dto: Message) -> None:
        self.yml_path = self._path(dto)

    def _path(self, dto: Message):
        if dto.metadata.rbc_flag is True:
            return self.DIR_PATH / "rbc.yml"
        actor, _ = dto.metadata.actor_behavior.split(".", maxsplit=1)
        return self.DIR_PATH / str(actor + ".yml")

    def _yml(self):
        with self.yml_path.open("r", encoding="utf-8") as file_obj:
            yml = safe_load(file_obj)
        return yml

    def controller_actors(self) -> Actors:
        """Controller Actor static data"""
        yml = self._yml()
        return Actors(actors=tuple(Actor.model_validate(a) for a in yml["actors"]))

    def rbc_cell_behavior_maps(self) -> CellBehaviorMaps:
        """RBC Actor static data
        - a tuple of cells id's that map to asscoiated actor behaviors"""
        yml = self._yml()
        return CellBehaviorMaps(
            maps=tuple(CellBehaviors.model_validate(m) for m in yml["maps"])
        )
