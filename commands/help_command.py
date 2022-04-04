from command import Command, CommandCode

class HelpCommand(Command):

    def __init__(self, manager, auth):
        super().__init__()
        self.name = "help"
        self.aliases = ["h"]
        self.manager = manager
        self.auth = auth

    def run(self) -> CommandCode:
        print("This is the help command")
        return CommandCode.SUCCESS

def setup(program) -> None:
    program.load_command(HelpCommand(program.manager, program.auth))
