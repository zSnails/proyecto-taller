from command import CommandCode, Command
from models import AccountRole, Account

class JohanCommand(Command):
    """Command interface for internal command handling"""
    
    def __init__(self):
        self.name = "johan"
        self.aliases = ["jh", "pn"]
        self.required_role = AccountRole.STUDENT
        self.description = "who knows what this might be"

    def run(self, ctx) -> CommandCode:
        print("el usuario se llama", self.user.name)
        print("me cago en todo")

def setup(program):
    program.load_command(JohanCommand())
