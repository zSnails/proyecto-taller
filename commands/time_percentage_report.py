from command import Command, CommandCode
from program import Program
from datetime import datetime
from colorama import Fore, Style


class TimePercentageReport(Command):
    def __init__(self):
        super().__init__()
        self.name = "time-percentage-report"
        self.aliases = ["tpr", "t"]
        self.description = "Shows a time percentage report"

    def run(self, ctx: Program) -> CommandCode:

        activities = [
            a
            for a in ctx.manager.activities
            if a.activity_date == datetime.today().date()
            and a.belongs_to == ctx.user.id
        ]

        total = len(activities)
        leisure_finished = len([a for a in activities if a.done and not a.course])
        if total:
            percentage = round((leisure_finished * 100) / total)

            print("Report for today's activities:")

            print(
                f"{Fore.LIGHTGREEN_EX}{percentage}%{Style.RESET_ALL} Of leisure activities are marked as done\n"
                f"{Fore.LIGHTRED_EX}{100 - percentage}%{Style.RESET_ALL} Of leisure activities are still unfinished"
            )

            print("=" * 20)

            bound_finished = len([a for a in activities if a.done and a.course])
            print(bound_finished)
            percentage = round((bound_finished * 100) / total)

            print(
                f"{Fore.LIGHTGREEN_EX}{percentage}%{Style.RESET_ALL} Of course bound activities are marked as done\n"
                f"{Fore.LIGHTRED_EX}{100 - percentage}%{Style.RESET_ALL} Of course bound activities are still unfinished"
            )

        else:
            print("There are no activities for today")

        return CommandCode.SUCCESS


def setup(program):
    program.load_command(TimePercentageReport())
