from command import Command, CommandCode
from program import Program
from arrow import get
from datetime import datetime
from colorama import Fore, Style

class ShowActivitiesCommand(Command):
    
    def __init__(self):
        super().__init__()
        self.name = "show-activities"
        self.aliases = ["sa", "sha"]
        self.description = "Show a list of your activities"
    
    def run(self, ctx: Program) -> CommandCode:
        current_activities = [activity for activity in ctx.manager.get_activities() if activity.id in ctx.user.activities]

        for activity in current_activities:
            human = get(activity.activity_date)
            print(f"[{activity.id}]", Fore.LIGHTGREEN_EX + human.humanize() + Style.RESET_ALL, activity.name, "\n\t- ", activity.description, "\nStatus: ", "done" if activity.done else "unfinished")

        return CommandCode.SUCCESS

def setup(program):
    program.load_command(ShowActivitiesCommand())
