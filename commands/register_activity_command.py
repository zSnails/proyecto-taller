from command import Command, CommandCode
from program import Program
from models import Activity
from datetime import datetime

class RegisterActivityCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "register-activity"
        self.aliases = ["ra", "na"]
    def run(self, ctx: Program) -> CommandCode:
        
        print("===== Registering an activity =======")

        name = input("Enter activity name> ")
        description = input("Enter activity description> ")
        
        course = input("Bind to course?> (y/n)> ")
        if course == 'y':
            for c in ctx.manager.get_courses(ctx.user.career):
                print(c.id, c.name)
            course = int(input("Enter course id> "))
            if course in ctx.user.passed or course in ctx.user.failed:
                print("Can't bind to a passed/failed course")
                return CommandCode.CONTINUE
        else:
            course = None
        

        activity_date = input("Enter start date (yyyy-mm-dd)> ")
        activity_date = datetime.strptime(activity_date, "%Y-%m-%d")
        
        # activity_duration = (end_date - start_date)
        begin_time = input("Start hour (h:m:s)> ")
        end_time = input("End hour (h:m:s)> ")
        
        begin_time = datetime.strptime(begin_time, "%H:%M:%S")
        end_time = datetime.strptime(end_time, "%H:%M:%S")
        
        # total_weekly_hours refers to the total amount of work hours for the current week
        total_weekly_hours = 0
        for _c in [c for c in ctx.manager.courses if c.id in ctx.user.courses and c.end_date > datetime.now().date() and c.start_date < datetime.now().date()]:
            total_weekly_hours += _c.weekly_hours
        
        if total_weekly_hours > 72:
            print("You can't have more than 72 hours of work on a single week!")
            return CommandCode.CONTINUE
        
        activity = Activity(
            id = len(ctx.manager.activities) + 1,
            name = name,
            belongs_to = ctx.user.id,
            description = description,
            course = course,
            activity_date = activity_date,
            done = False,
            start_hour = begin_time.time(),
            end_hour = end_time.time()
        )
        
        ctx.manager.register_activity(activity)
        return CommandCode.SUCCESS

def setup(program):
    program.load_command(RegisterActivityCommand())