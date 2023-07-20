import kazparse

p = kazparse.Parse(
    name="ProgramName", before="Text before help", after="Text after help"
)


class Color:
    def __init__(self, color):
        self.r = color[0] + color[1]
        self.g = color[2] + color[3]
        self.b = color[4] + color[5]


p.flag(
    "color", short="c", long="color", help="Specify color to use", type=Color
)  # example for specifying color
p.flag(
    "color2",
    short="C",
    long="color2",
    help="Specify a second color to use",
    type=Color,
    default=Color("f0f0f0"),
)  # example for specifying default argument


@p.command("CommandName")
def commandName(flags, arg1, arg2):
    "Help that is printed for CommandName"
    pass


@p.command("grabAll")
def grab_all(flags, *args):
    "Grabs all arguments"
    pass


@p.command("printColor", required=["color"])
def printColor(flags):
    "Prints Color given with --color"
    print(flags.color.r, flags.color.g, flags.color.b)
    print(flags.color2.r, flags.color2.g, flags.color2.b)


p.run()
