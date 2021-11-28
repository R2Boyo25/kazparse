"""
Contains Command class
"""

class FlagError(Exception):
    pass

class Command:
    def __init__(self, name, func, args = [], help = "", required = []):
        self._name = name
        self._func = func
        self._help = help.strip('\n').strip() if help else ""
        self._args = args
        self._required = required

    def _splitOnLongLine(self, text, length):
        out = []
        buf = []
        for pos, char in enumerate(text):
            buf.append(char)
            if pos > length:
                out.append("".join(buf))
                buf = []

        out.append("".join(buf))
        return out

    def pretty(self, indent = 8, longest_command = 2, screen_width = 10):
        return f"\n{' '*indent}".join(self._splitOnLongLine(f"{' ' * indent}{self._name}{' ' * (longest_command - len(self._name))} | {self._help}", screen_width))
    
    def run(self, *args, **kwargs):
        for requirement in self._required:
            if args[0][requirement] is None:
                if len(requirement) > 1:
                    raise FlagError(f"Flag --{requirement} is required by {self._name}")
                else:
                    raise FlagError(f"Flag -{requirement} is required by {self._name}")

        self._func(*args, **kwargs)
        