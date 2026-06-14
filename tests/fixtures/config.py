from pytest import fixture
from shared.config.locker import Locker


@fixture(scope="session", name="locker")
def f_locker():
    return Locker()


@fixture(scope="session", name="config_log")
def f_config_log(locker):
    return locker.log()


@fixture(scope="session", name="config_api")
def f_config_achat(locker):
    return locker.api()
