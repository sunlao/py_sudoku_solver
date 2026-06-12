from pathlib import Path
from yaml import safe_load
from shared.models.static_data import Actors, Actor


class Read:
    DIR_PATH = Path(__file__).resolve().parent

    def __init__(self, file: str) -> None:
        self.yml_path = self.DIR_PATH / str(file + '.yml')

    def _yml(self):
        with self.yml_path.open("r", encoding="utf-8") as file_obj:
            yml = safe_load(file_obj)
        return yml

    def get_controller(self) -> Actors:
        yml = self._yml()
        return Actors(
            actors=tuple(
                Actor.model_validate(actor)
                for actor in yml["actors"]
            )
        )
