from command import Command, CommandCode

class ExitCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "exit"
        self.aliases = ["q", "quit"]

    def run(self) -> CommandCode:
        return CommandCode.EXIT

def setup(program) -> None:
    program.load_command(ExitCommand())
