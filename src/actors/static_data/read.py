from pathlib import Path
from yaml import safe_load
from shared.models.static_data import StaticDataInit, Actors, Actor, Route, RouteName


class Read:
    """Get static yml data by file name as a Data Transport Object (DTO)"""

    DIR_PATH = Path(__file__).resolve().parent

    def __init__(self, dto: StaticDataInit) -> None:
        self.yml_path = self.DIR_PATH / str(dto.name + ".yml")

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
        """Lookup route static data for shared handler by route name"""
        yml = self._yml()
        route = next(r["route"] for r in yml["routes"] if r["name"] == dto.name)
        return Route(route=route)
