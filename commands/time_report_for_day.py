from command import Command, CommandCode
from program import Program
from datetime import datetime
from arrow import get
# import arrow
class TimeReportForDayCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "time-report-for-day"
        self.aliases = ["trfd"]
        
    def run(self, ctx: Program) -> CommandCode:
        
        today_int = datetime.today().weekday() + 1
        
        users_courses = [c for c in ctx.manager.courses if c.id in ctx.user.courses]
        # NOTE: black magic happens here
        todays_courses = sum([(datetime.strptime(str(sch[2]), "%H:%M:%S") - datetime.strptime(str(sch[1]), "%H:%M:%S")).total_seconds() / 3600 for course in users_courses for sch in course.schedule if sch[0] == today_int])

        users_activities = [a for a in ctx.manager.activities if a.belongs_to == ctx.user.id]
        todays_activities = sum([(datetime.strptime(str(activity.end_hour), "%H:%M:%S") - datetime.strptime(str(activity.start_hour), "%H:%M:%S")).total_seconds() / 3600 for activity in users_activities if activity.activity_date == datetime.today().date()])

        used_hours = todays_courses + todays_activities
        
        print(f"Free and used time report for today:\nFree time: {24-used_hours}\nUsed time: {used_hours}")      
        
        
        
        return CommandCode.SUCCESS

def setup(program):
    program.load_command(TimeReportForDayCommand())