from os import getenv
from os.path import join
from datetime import datetime
from time import perf_counter
from uuid import uuid4
from shared.models.api import API
from shared.models.log import Config


class NoValidEnvironment(Exception):
    """Raised when an unsupported ENV system variable is set."""

    def __init__(self, env: str, message: str = "Only dev and ci are supported"):
        super().__init__(f"System ENV variable: {env}. {message}")


class Locker:
    """Configs and Secrets managed at the Edge"""

    def __init__(self):
        self.true_values = ("1", "true", "yes", "on", 1)
        self.env = getenv("ENV", "false")

    @staticmethod
    def _app_version() -> str:
        path = "/app/VERSION"
        with open(path, encoding="UTF-8") as file_obj:
            version = file_obj.read()
        return version

    def api(self) -> API:
        return API(app_version=self._app_version())

    def log(self) -> Config:
        """Log Config"""
        log_to_file = getenv("LOG_TO_FILE", "true").strip().lower() in self.true_values
        if self.env in {"dev", "ci"}:
            return Config(
                Level=getenv("LOG_LEVEL"),
                Service=getenv("SERVICE"),
                LogToFile=log_to_file,
                LogDirectory=join(getenv("LOG_DIR"), f"{getenv('SERVICE')}.log"),
                BackUpCount=int(getenv("BACKUP_COUNT", "10")),
                Environment=self.env,
                Now=datetime.now,
                TimeCounter=perf_counter,
                UUID4=uuid4,
            )
        raise NoValidEnvironment(self.env)
