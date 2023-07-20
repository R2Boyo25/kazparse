from importlib import import_module
import os, sys

from typing import Any, Callable


def getAttrs(plugin: Any) -> list[str]:
    filteredattrs = []

    for attr in dir(plugin):
        if not attr.startswith("_"):
            filteredattrs.append(attr)

    return filteredattrs


def loadPlugins(plugindir: str = "commands") -> list[Any]:
    plugins = []

    sys.path.insert(0, os.path.dirname(os.path.realpath(sys.argv[0])))

    plugindireeeeeeee = os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + plugindir

    pluginfiles = os.listdir(plugindireeeeeeee)

    pluginfiles = [
        i for i in pluginfiles if os.path.isfile(f"{plugindireeeeeeee}/" + i)
    ]

    for pluginfile in pluginfiles:
        plugin = import_module(
            f"{plugindir.replace('/', '.')}." + pluginfile.split(".")[0]
        )
        plugins.append(plugin)

    return plugins


def getHandlers(plugins: list[Any]) -> dict[str, list[Callable[[Any], Any]]]:
    handlers: dict[str, list[Callable[[Any], Any]]] = {}

    for plugin in plugins:
        for handlername in getAttrs(plugin):
            if handlername.startswith("_"):
                continue

            handler = getattr(plugin, handlername)

            if str(type(handler)) != "<class 'function'>":
                continue

            if not handlername in handlers.keys():
                handlers[handlername] = []

            handlers[handlername].append(handler)

    return handlers
