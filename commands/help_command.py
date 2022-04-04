from command import Command, CommandCode

class HelpCommand(Command):

    def __init__(self):
        self.name = "help"
        self.aliases = ["h"]

    def run(self) -> CommandCode:
        print("This is the help command")
        return CommandCode.SUCCESS

def setup(program) -> None:
    program.load_command(HelpCommand())
