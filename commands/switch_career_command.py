from command import Command, CommandCode
from program import Program


class SwitchCareerCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "switch-career"
        self.aliases = ["sc", "swc"]
        self.description = "Lets the user switch career"

    def run(self, ctx: Program) -> CommandCode:

        for c in ctx.manager.careers:
            print(f"[{c.id}] - ", c.name)
        chosen = input("Enter the career you want to switch to> ")

        ctx.manager.switch_account_career(account_id=ctx.user.id, career_id=int(chosen))
        ctx.manager.reset_account_courses(account_id=ctx.user.id)
        account = ctx.manager.get_account(id=ctx.user.id)
        if not account:
            return CommandCode.CONTINUE

        ctx.user = account

        return CommandCode.SUCCESS


def setup(program):
    program.load_command(SwitchCareerCommand())
