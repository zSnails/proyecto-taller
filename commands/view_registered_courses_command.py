from command import Command, CommandCode
from program import Program
from colorama import Fore, Style


class ViewRegisteredCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "view-courses"
        self.aliases = ["vc"]
        self.description = "Shows a list of registered courses"

    def run(self, ctx: Program) -> CommandCode:
        for course in ctx.manager.get_account_courses(id=ctx.user.id):

            end = ""

            if course.id in ctx.user.passed:
                end = f"- {Fore.LIGHTGREEN_EX}passed{Style.RESET_ALL}"
            elif course.id in ctx.user.failed:
                end = f"- {Fore.LIGHTRED_EX}failed{Style.RESET_ALL}"

            print(course.id, course.name, end)

        return CommandCode.SUCCESS


def setup(program):
    program.load_command(ViewRegisteredCommand())
