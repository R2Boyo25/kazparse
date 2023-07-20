from .plugins import getHandlers, loadPlugins

from typing import Callable, Any
from kazparse.flags import Flags


class Loader:
    def __init__(self, parser: Any, directory: str = "commands"):
        self.parser = parser
        self.handlers = getHandlers(loadPlugins(directory))
        try:
            self.handlers["load"]
        except:
            pass
        else:
            for loader in self.handlers["load"]:
                loader(self)

    def add(self, function: Callable[[Flags, Any], None], name: str) -> None:
        self.parser.command(name)(function)
