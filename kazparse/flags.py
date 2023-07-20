"""
Contains Flags class
"""

from typing import Any


class Flags:
    "Class that is used to give the values of flags to a command"

    def __init__(self, flags: dict[str, Any]):
        self._values = flags

    def __getattr__(self, attr: str) -> Any:
        return self._values[attr]

    def __getitem__(self, item: str) -> Any:
        return self._values[item]

    def __str__(self) -> str:
        return str(self._values)
