from command import Command, CommandCode
from colorama import Fore, Style
from typing import Dict
class HelpCommand(Command):

    def __init__(self):
        super().__init__()
        self.name = "help"
        self.aliases = ["h"]
        self.description = "Show this message!"

    def run(self, ctx) -> CommandCode:
        for command in ctx.commands.values():
            if command.required_role > ctx.user.role: continue
            print(Fore.GREEN, command.name, Style.RESET_ALL, ": ", command.description, "\nAliases: ", command.aliases, sep="")
        return CommandCode.SUCCESS

def setup(program):
    program.load_command(HelpCommand())
