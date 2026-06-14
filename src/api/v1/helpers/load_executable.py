from collections.abc import Callable
from importlib import import_module


def load_executable(route: str) -> Callable:
    module_path, class_name, method_name = route.rsplit(".", 2)
    cls = getattr(import_module(module_path), class_name)
    return getattr(cls(), method_name)
