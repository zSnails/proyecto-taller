from command import Command, CommandCode
from program import Program

class SwitchCareerCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "switch-career"
        self.aliases = ["sc", "swc"]

    def run(self, ctx: Program) -> CommandCode:
        
        for c in ctx.manager.careers:
            print(f"[{c.id}] - ", c.name)
        chosen = input("Enter the career you want to switch to> ")
        
        ctx.manager.switch_account_career(account_id=ctx.user.id, career_id=int(chosen))
        ctx.manager.reset_account_courses(account_id=ctx.user.id)
        
        ctx.user = ctx.manager.get_account(id=ctx.user.id) 
        return CommandCode.SUCCESS

def setup(program):
    program.load_command(SwitchCareerCommand())
