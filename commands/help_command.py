from command import Command, CommandCode
from colorama import Fore, Style
from typing import Dict
class HelpCommand(Command):

    def __init__(self):
        super().__init__()
        self.name = "help"
        self.aliases = ["h"]

    def run(self, ctx) -> CommandCode:
        for command in ctx.commands.values():
            print(Fore.GREEN, command.name, Style.RESET_ALL, ": ", command.description, sep="")
        return CommandCode.SUCCESS

def setup(program):
    program.load_command(HelpCommand())
