"""
Contains Command class
"""

class FlagError(Exception):
    pass

class Command:
    def __init__(self, name, func, args = [], help = "", required = [], hidden = False):
        self._name = name
        self._func = func
        self._help = help.strip('\n').strip() if help else ""
        self._args = args
        self._required = required
        self.hidden = hidden

    def _splitOnLongLine(self, text, length, indent):
        out         = []
        buf         = []
        length     -= 2
        totalindent = 0
        totalchars  = 0

        for pos, char in enumerate(text):
            if char != "\n":
                buf.append(char)
                
            if ( pos - totalchars > length - totalindent ) or ( char == "\n" ):
                out.append("".join(buf))
                totalchars += len(buf)
                buf = []
                totalindent = indent

        out.append("".join(buf))
        return out

    def pretty(self, indent = 8, longest_command = 2, screen_width = 10):
        continuing_indent = indent + longest_command + 3
        
        return f"\n{' '*(continuing_indent)}".join(self._splitOnLongLine(f"{' ' * indent}{self._name}{' ' * (longest_command - len(self._name))} | {self._help}", screen_width, continuing_indent))
    
    def run(self, *args, **kwargs):
        for requirement in self._required:
            if args[0][requirement] is None:
                if len(requirement) > 1:
                    raise FlagError(f"Flag --{requirement} is required by {self._name}")
                else:
                    raise FlagError(f"Flag -{requirement} is required by {self._name}")

        self._func(*args, **kwargs)
        
    def __lt__(self, other):
        if self._name and other._name:
            return self._name > other._name
        else:
            return False
