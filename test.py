import CLIParse

p = CLIParse.Parse("test", before = "Test Program V1.0", after = "This is the after text", flagsAsArgumentsAfterCommand = True)

p.flag("b", short = "b", long = "brown", help = "Whether to be brown")
p.flag("p", short = "p", long = "purple", help = "Whether to be purple")
p.flag("c", short = "c", long = "color", help = "Color to use", type = str)

@p.command("pargs")
def printArgs(flags, *args):
    "Print arguments"
    print(flags, *args)

@p.command()
def defaultCommand(flags, *args):
    print(flags, *args)

p.run()