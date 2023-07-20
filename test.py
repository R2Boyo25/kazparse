import kazparse

p = kazparse.Parse(
    "test",
    before="Test Program V1.0\nmultiline before",
    after="This is the after text\nnewline",
    flagsAsArgumentsAfterCommand=True,
)

p.flag("b", short="b", long="brown", help="Whether to be brown\nnewline")
p.flag("p", short="p", long="purple", help="Whether to be purple")
p.flag("c", short="c", long="color", help="Color to use", type=str)
p.flag("single", long="single", help="Test for sorting single arguments")


@p.command("pargs")
def printArgs(flags, *args):
    "Print arguments\nmultilinehelp\nanother line"
    print(flags, *args)


@p.command("sort")
def sortCommand(flags, *args):
    "Test command sorting"


@p.command()
def defaultCommand(flags, *args):
    print(flags, *args)


p.run()
