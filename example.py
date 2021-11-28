import CLIParse

p = CLIParse.Parse(name = "ProgramName", before = "Text before help", after = "Text after help")

class Color:
    def __init__(self, color):
        self.r = color[0] + color[1]
        self.g = color[2] + color[3]
        self.b = color[4] + color[5]

p.flag("color", short = "c", long = "color", help = "Specify color to use", type = Color) # example for specifiying color


@p.command("CommandName")
def commandName(flags, arg1, arg2):
    "Help that is printed for CommandName"
    pass

@p.command("grabAll")
def grab_all(flags, *args):
    "Grabs all arguments"
    pass

@p.command("printColor")
def printColor(flags):
    "Prints Color given with --color"
    if flags.color:
        print(flags.color.r, flags.color.g, flags.color.b)
    else:
        print("Need a color to print!")

p.run()