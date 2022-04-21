from command import Command, CommandCode
from models import Career, AccountRole
class RegisterCareerCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "register-career"
        self.aliases = ["rc"]
        self.description = "Starts the career registration daemon"
        self.required_role = AccountRole.ADMIN
        
    def run(self, ctx) -> CommandCode:
        print("====== Registering a new course =======")
        
        name = input("Enter career name>")
        # if name in ctx.manager.courses:
        #   print("Ese curso ya existe")
        #   return CommandCode.Error
        ctx.manager.register_career(Career(id = len(ctx.manager.careers) +1, name = name))
        return CommandCode.SUCCESS
    
def setup(program):
    program.load_command(RegisterCareerCommand())