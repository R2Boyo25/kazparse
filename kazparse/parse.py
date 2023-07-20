"""
Contains Parse class
"""


from .flag import Flag
from .command import Command, FlagError
from .flags import Flags
import sys
import os
import traceback
from .loader import Loader

from typing import Callable, Any, Sequence


class ArgumentError(Exception):
    pass


class Parse:
    def __init__(
        self,
        name: str = sys.argv[0],
        before: None | str = None,
        after: None | str = None,
        flagsAsArgumentsAfterCommand: bool = False,
    ):
        self.name = name
        self.before_text = before
        self.after_text = after
        self.flagsAsArgumentsAfterCommand = flagsAsArgumentsAfterCommand
        self.flags: list[Flag] = []
        self.rflags: dict[str, Any] = {}
        self.commands: list[Command] = []
        self.inArg = False
        self.inArgName = ""
        self.ccommand = ""
        self.gotcommand = False
        self.pargs: list[str] = []

    def loadDir(self, directory: str = "commands") -> None:
        if type(directory) == list:  # type: ignore
            for _directory in directory:
                Loader(self, _directory)
        elif type(directory) == str:
            Loader(self, directory)

    def flag(self, *args: Any, **kwargs: Any) -> None:
        self.flags.append(Flag(*args, **kwargs))
        self.flags.sort()

    def command(
        self, commandname: str = "", required: list[str] = [], hidden: bool = False
    ) -> Callable[[Callable[[Flags, Any], None]], None]:
        def decorator_command(function: Callable[[Flags, Any], None]) -> None:
            self.commands.append(
                Command(
                    commandname,
                    function,
                    args=list(function.__code__.co_varnames),
                    help=function.__doc__ if function.__doc__ else "",
                    required=required,
                    hidden=hidden,
                )
            )

        self.commands.sort()
        return decorator_command

    def _getLongestFlag(self) -> int:
        longest = 0
        for flag in self.flags:
            if flag._long:
                if len(flag._long) > longest:
                    longest = len(flag._long)

        return longest

    def _getLongestCommand(self) -> int:
        longest = 0
        for command in self.commands:
            if len(command._name) > longest:
                longest = len(command._name)

        return longest

    def _getCommands(self) -> list[str]:
        coms = []
        for command in self.commands:
            coms.append(command._name)

        return coms

    def _getCommand(self, commandname: str) -> Command | None:
        for command in self.commands:
            if command._name == commandname:
                return command
        else:
            return None

    def _getScreenWidth(self) -> int:
        return os.get_terminal_size()[0]

    def _cluster(self) -> str:
        out = ""
        for flag in self.flags:
            if flag._short:
                out += flag._short

        return out

    def _numOfShortArgs(self) -> int:
        out = 0
        for flag in self.flags:
            if flag._short:
                out += 1

        return out

    def _numOfLongArgs(self) -> int:
        out = 0
        for flag in self.flags:
            if flag._long:
                out += 1

        return out

    def _prettyLongArgs(self) -> list[str]:
        out = [""]
        for flag in self.flags:
            if flag._long:
                out.append("[" + "--" + flag._long + "]")

        return out

    def _getNamedCommands(self) -> int:
        out = 0
        for command in self.commands:
            if command._name != "" and not command.hidden:
                out += 1
        return out

    def _getLongest(self) -> int:
        if self._getLongestCommand() > self._getLongestFlag() + 5:
            return self._getLongestCommand()
        else:
            return self._getLongestFlag() + 5

    def _splitOnLongLine(self, text: str, length: int, indent: int = 4) -> list[str]:
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

    def _usage(self) -> None:
        print("Usage:")
        name = self.name
        indent = 3 * " "
        if (
            self._numOfShortArgs() > 0
            and self._numOfLongArgs() > 0
            and self._getNamedCommands() > 0
        ):
            usage = (
                indent,
                f"{name} [-{self._cluster()}]{' '.join(self._prettyLongArgs())} [command]",
            )
        elif self._numOfShortArgs() > 0 and self._numOfLongArgs() > 0:
            usage = (
                indent,
                f"{name} [-{self._cluster()}]{' '.join(self._prettyLongArgs())}",
            )
        elif self._numOfShortArgs() > 0 and self._getNamedCommands() > 0:
            usage = (indent, f"{name} [-{self._cluster()}] [command]")
        elif self._numOfShortArgs() > 0 and self._getNamedCommands() > 0:
            usage = (indent, f"{name} [-{self._cluster()}] [command]")
        elif self._numOfLongArgs() > 0:
            usage = (indent, f"{name} {' '.join(self._prettyLongArgs())}")
        elif self._getNamedCommands() > 0:
            usage = (indent, f"{name} [command]")
        else:
            usage = (indent, f"{name}")

        joined_usage = " ".join(usage)
        joined_usage = ("\n" + " " * 4).join(
            self._splitOnLongLine(joined_usage, self._getScreenWidth())
        )
        print(joined_usage)

    def _help(self, commandname: str | None = None) -> None:
        if self.before_text:
            print(
                ("\n" + " " * 4).join(
                    self._splitOnLongLine(
                        self.before_text,
                        self._getScreenWidth(),
                        indent=8 + self._getLongest(),
                    )
                )
                + "\n"
            )

        if commandname:
            if (command := self._getCommand(commandname)) is not None:
                print(command._help)
            else:
                print(f"Command {commandname} does not exist")
        else:
            self._usage()

            if self._getNamedCommands() > 0:
                print("Commands:")
                for command in self.commands:
                    if not command.hidden:
                        print(
                            command.pretty(
                                indent=8,
                                longest_command=self._getLongest(),
                                screen_width=self._getScreenWidth(),
                            )
                            .rstrip()
                            .rstrip("|")
                            .rstrip()
                        )
            if len(self.flags) > 0:
                print("Flags:")
                for flag in self.flags:
                    print(
                        flag.pretty(
                            indent=8,
                            longest_long=self._getLongest(),
                            screen_width=self._getScreenWidth(),
                        )
                        .rstrip()
                        .rstrip("|")
                        .rstrip()
                    )

        if self.after_text:
            print(
                "\n"
                + ("\n" + " " * 4).join(
                    self._splitOnLongLine(
                        self.after_text, self._getScreenWidth(), indent=4
                    )
                )
            )

        sys.exit()

    def _getFlag(self, flagname: str) -> Flag:
        for flag in self.flags:
            if flag._short == flagname or flag._long == flagname:
                return flag
        else:
            if len(flagname) == 1:
                raise ArgumentError(f"Invalid flag -{flagname}")
            else:
                raise ArgumentError(f"Invalid flag --{flagname}")

    def handleArg(self, pos: int, args: list[str]) -> None:
        try:
            arg = args[pos]

            if not self.inArg and self.gotcommand and self.flagsAsArgumentsAfterCommand:
                self.pargs.append(arg)
                return

            if arg.lower() in ["-h", "--help", "help"]:
                self._help()

            if arg.startswith("--"):
                flag = arg.lstrip("--")
                arg = arg.lstrip("--")

                if "=" in flag and flag[-1] != "=":
                    flag = arg.split("=")[0]

                    if self._getFlag(flag)._type:
                        self.inArg = True
                        self.inArgName = arg.split("=")[-1]

                    else:
                        raise ArgumentError(f"Flag --{flag} is a toggle")

                elif flag[-1] == "=":
                    flag = arg.rstrip("=")

                    if self._getFlag(flag)._type:
                        self.inArg = True
                        self.inArgName = flag

                    else:
                        raise ArgumentError(f"Flag --{flag} is not a toggle")

                else:
                    flag = arg.rstrip("=")

                    if self._getFlag(flag)._type:
                        self.inArg = True
                        self.inArgName = flag

                    else:
                        if pos == len(args) - 1:
                            if "=" in arg:
                                raise ArgumentError(f"Flag --{flag} is a toggle")

                        else:
                            if "=" in arg or args[pos + 1].startswith("="):
                                raise ArgumentError(f"Flag --{flag} is a toggle")

                        self.rflags[self._getFlag(flag)._name] = True

            elif arg.startswith("-") and arg[1] not in [str(i) for i in range(10)]:
                arg = arg.lstrip("-")

                if "=" in arg and arg[-1] != "=":
                    flag = arg.split("=")[0]

                    if self._getFlag(flag)._type:
                        self.rflags[self._getFlag(flag)._name] = arg.split("=")[-1]

                    else:
                        raise ArgumentError(f"Flag -{flag} is a toggle")

                elif arg[-1] == "=":
                    flag = arg.rstrip("=")

                    if self._getFlag(flag)._type:
                        self.inArg = True
                        self.inArgName = flag

                    else:
                        raise ArgumentError(f"Flag -{flag} is not a toggle")

                elif len(arg) > 1:
                    for flag in arg:
                        if self._getFlag(flag)._type:
                            self.inArg = True
                            self.inArgName = arg

                        else:
                            self.rflags[self._getFlag(flag)._name] = True

                else:
                    flag = arg.rstrip("=")

                    if self._getFlag(flag)._type:
                        self.inArg = True
                        self.inArgName = flag

                    else:
                        if pos == len(args) - 1:
                            if "=" in arg:
                                raise ArgumentError(f"Flag --{flag} is a toggle")

                        else:
                            if "=" in arg or args[pos + 1].startswith("="):
                                raise ArgumentError(f"Flag --{flag} is a toggle")

                        self.rflags[self._getFlag(flag)._name] = True

            else:
                if not self.inArg:
                    if self.gotcommand:
                        self.pargs.append(arg)

                    else:
                        if arg in self._getCommands():
                            self.ccommand = arg
                            self.gotcommand = True

                        else:
                            if not ("" in self._getCommands()):
                                raise ArgumentError(f"Invalid command {arg}")

                            else:
                                self.pargs.append(arg)
                                self.gotcommand = True

                else:
                    if arg.strip() != "=":
                        self.inArg = False
                        self.rflags[
                            self._getFlag(self.inArgName)._name
                        ] = self._getFlag(self.inArgName).parse(arg.lstrip("=").strip())

        except ArgumentError as e:
            print(e)
            self._help()

    def run(
        self, args: Sequence[str] | None = None, extras: Any | None = None
    ) -> None:
        if not args:
            args = sys.argv[1:]

        for flag in self.flags:
            if flag._default:
                self.rflags[flag._name] = flag._default
            else:
                self.rflags[flag._name] = None

        if len(args) == 0 and (not "" in self._getCommands()):
            self._help()

        for obj in enumerate(args):
            pos = obj[0]
            self.handleArg(pos, args)

        if self.inArg:
            if len(self.inArgName) > 1:
                print(f"Flag --{self.inArgName} is not a toggle")
            else:
                print(f"Flag -{self.inArgName} is not a toggle")
            self._help()

        if (command := self._getCommand(self.ccommand)) is not None:
            try:
                if extras:
                    command.run(Flags(self.rflags), extras, *self.pargs)
                else:
                    command.run(Flags(self.rflags), *self.pargs)
            except FlagError as e:
                print(e)
                self._help()
        else:
            print("Specify a subcommand")
            self._help()
