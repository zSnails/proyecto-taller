from command import Command, CommandCode
from program import Program


class SwitchReportTypeCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "switch-report-type"
        self.aliases = ["srt", "swrt"]

    def run(self, ctx: Program) -> CommandCode:
        ctx.manager.switch_account_report_type(ctx.user.id)
        print("Sucessfully switched report type, restart to see changes")
        
        return CommandCode.SUCCESS
def setup(program):
    program.load_command(SwitchReportTypeCommand())