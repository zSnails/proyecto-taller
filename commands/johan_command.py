from command import CommandCode, Command
from models import AccountRole, Account

class JohanCommand(Command):
    """Command interface for internal command handling"""
    
    def __init__(self, user: Account):
        self.name = "johan"
        self.aliases = ["jh", "pn"]
        self.required_role = AccountRole.STUDENT
        self.user = user

    def run(self) -> CommandCode:
        print("el usuario se llama", self.name)
        print("me cago en todo")

def setup(program):
    program.load_command(JohanCommand(program.user))