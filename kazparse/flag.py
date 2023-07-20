"""
Contains Flag class
"""

from typing import Any


class Flag:
    def __init__(
        self,
        name: str,
        short: str | None = None,
        long: str | None = None,
        type: Any | None = None,
        help: str = "",
        default: Any | None = None,
    ):
        self._name = name
        self._short = short
        self._long = long
        self._type = type
        self._help = help
        self._default = default

    def parse(self, text: str) -> Any:
        if self._type:
            return self._type(text)
        else:
            return True

    def __str__(self) -> str:
        if self._short and self._long:
            return f"-{self._short} --{self._long} {self._help}"
        elif self._short:
            return f"-{self._short} {self._help}"
        elif self._long:
            return f"--{self._long} {self._help}"

        return ""

    def _splitOnLongLine(self, text: str, length: int, indent: int) -> list[str]:
        out = []
        buf = []
        length -= 2
        totalindent = 0
        totalchars = 0

        for pos, char in enumerate(text):
            if char != "\n":
                buf.append(char)

            if (pos - totalchars > length - totalindent) or (char == "\n"):
                out.append("".join(buf))
                totalchars += len(buf)
                buf = []
                totalindent = indent

        out.append("".join(buf))
        return out

    def pretty(
        self, indent: int = 8, longest_long: int = 2, screen_width: int = 10
    ) -> str:
        longest_long = longest_long - 5

        continuing_indent = indent + longest_long

        if self._short and self._long:
            return f"\n{' '*(continuing_indent)}".join(
                self._splitOnLongLine(
                    f"{' ' * indent}-{self._short} --{self._long}{' ' * (longest_long - len(self._long))} | {self._help}".replace(
                        "\n", f"\n{' '*indent}"
                    ),
                    screen_width,
                    continuing_indent,
                )
            )
        elif self._short:
            return f"\n{' '*(continuing_indent)}".join(
                self._splitOnLongLine(
                    f"{' ' * indent}-{self._short}{' ' * (longest_long+3)} | {self._help}".replace(
                        "\n", f"\n{' '*indent}"
                    ),
                    screen_width,
                    continuing_indent,
                )
            )
        elif self._long:
            return f"\n{' '*(continuing_indent)}".join(
                self._splitOnLongLine(
                    f"{' ' * indent}   --{self._long}{' ' * (longest_long - len(self._long))} | {self._help}".replace(
                        "\n", f"\n{' '*indent}"
                    ),
                    screen_width,
                    continuing_indent,
                )
            )

        return ""

    def __lt__(self, other: "Flag") -> bool:
        if self._short and other._short:
            return self._short < other._short
        elif self._long and other._long:
            return self._long < other._long
        else:
            return self._name < other._name
