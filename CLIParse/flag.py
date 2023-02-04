"""
Contains Flag class
"""

class Flag:
    def __init__(self, name, short = None, long = None, type = None, help = "", default = None):
        self._name = name
        self._short = short
        self._long = long
        self._type = type
        self._help = help
        self._default = default
    
    def parse(self, text):
        if self._type:
            return self._type(text)
        else:
            return True
    
    def __str__(self):
        if self._short and self._long:
            return f"-{self._short} --{self._long} {self._help}"
        elif self._short:
            return f"-{self._short} {self._help}"
        elif self._long:
            return f"--{self._long} {self._help}"
    
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

    def pretty(self, indent = 8, longest_long = 2, screen_width = 10):
        longest_long = longest_long - 5

        continuing_indent = indent + longest_long
        
        if self._short and self._long:
            return f"\n{' '*(continuing_indent)}".join(self._splitOnLongLine(f"{' ' * indent}-{self._short} --{self._long}{' ' * (longest_long - len(self._long))} | {self._help}".replace("\n", f"\n{' '*indent}"), screen_width, continuing_indent))
        elif self._short:
            return f"\n{' '*(continuing_indent)}".join(self._splitOnLongLine(f"{' ' * indent}-{self._short}{' ' * (longest_long+3)} | {self._help}".replace("\n", f"\n{' '*indent}"), screen_width, continuing_indent))
        elif self._long:
            return f"\n{' '*(continuing_indent)}".join(self._splitOnLongLine(f"{' ' * indent}   --{self._long}{' ' * (longest_long - len(self._long))} | {self._help}".replace("\n", f"\n{' '*indent}"), screen_width, continuing_indent))

    def __lt__(self, other):
        if self._short and other._short:
            return self._short < other._short
        elif self._long and other._long:
            return self._long < other._long
        else:
            return self._name < other._name
