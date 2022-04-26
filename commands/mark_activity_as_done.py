from command import Command, CommandCode
from program import Program

class MarkActivityAsDone(Command):
    def __init__(self):
        super().__init__()
        self.name = "mark-activity-as-done"
        self.aliases = ["masd"]
        self.description = "Lets you mark an activity as done"

    def run(self, ctx: Program):
        
        for activity in ctx.manager.activities:
            if activity.id in ctx.user.activities:
                print(activity.id, activity.name)
        
        activity_id = input("Enter the id of the activity to mark as done> ")
        
        
        ctx.manager.update_activity(int(activity_id))
        
        return CommandCode.SUCCESS

def setup(program):
    program.load_command(MarkActivityAsDone())
