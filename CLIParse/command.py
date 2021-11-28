"""
Contains Command class
"""

class Command:
    def __init__(self, name, func, args = [], help = ""):
        self._name = name
        self._func = func
        self._help = help.strip('\n').strip() if help else ""
        self._args = args

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
        self._func(*args, **kwargs)
        