from pathlib import Path
from yaml import safe_load
from shared.models.constants import StaticDataNames
from shared.models.static_data import Actors, Actor, Route, RouteName


class Read:
    """Get static yml data by file name as a Data Transport Object (DTO)"""

    DIR_PATH = Path(__file__).resolve().parent

    def __init__(self, name: StaticDataNames) -> None:
        self.yml_path = self.DIR_PATH / str(name + ".yml")

    def _yml(self):
        with self.yml_path.open("r", encoding="utf-8") as file_obj:
            yml = safe_load(file_obj)
        return yml

    def controller_actors(self) -> Actors:
        """Controller Actor static data"""
        yml = self._yml()
        return Actors(
            actors=tuple(Actor.model_validate(actor) for actor in yml["actors"])
        )

    def handler_routes(self, dto: RouteName) -> Route:
        """Route static data for shared handler"""
        yml = self._yml()
        route = next(r["route"] for r in yml["routes"] if r["name"] == dto.name)
        return Route(route=route)
