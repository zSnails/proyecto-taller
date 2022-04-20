from command import Command, CommandCode
from models import Course, AccountRole, WeekDays
from datetime import timedelta, datetime, time, date
class RegisterCourseCommand(Command):

    def __init__(self):
        super().__init__()
        self.name = "register-course"
        self.aliases = ["new-course", "nc"]
        self.required_role = AccountRole.ADMIN

    def run(self, ctx) -> CommandCode:
        print("======= Registering a course =======")
        name = input("Course name> ")
        _credits = int(input("Course credits> "))

        start_date = input("Start date (yyyy-mm-dd)> ")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

        end_date = input("End date (yyyy-mm-dd)> ")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        course_weeks = (end_date - start_date)

        course_hours = 0
        weekly_hours = 0
        print("=== Set schedule ===")
        while True:
            for idx, weekday in enumerate(WeekDays):
                print(idx + 1, str(weekday).split(".").pop())
            day = input("Class day (enter day number) ('done' when finished)> ")
            if day == 'done':
                break
            begin = input("Start hour (h:m:s)> ")
            end = input("End hour (h:m:s)> ")

            day = WeekDays(int(day))
            begin = datetime.strptime(begin, "%H:%M:%S")
            end = datetime.strptime(end, "%H:%M:%S")

            weekly_hours += (end - begin).total_seconds() / 3600

        print(weekly_hours)


        # while True:
        #     class_day = input("Class date and start, end time (yyyy-mm-dd h:m:s h:m:s) ('done' when ready)> ")
        #     if class_day == 'done':
        #         break
        #     class_day = class_day.split(" ")
        #     print(class_day)
        #     day, start, end = class_day

        #     day = date(*[int(x) for x in day.split("-")])
        #     print(day)
        #     start = time(*[int(x) for x in start.split(":")])
        #     end = time(*[int(x) for x in end.split(":")])

        #     schedule.append((day, start, end))

        #     start = timedelta(start.hour, start.minute, start.second)
        #     end = timedelta(end.hour, end.minute, end.second)

        #     diff = end - start
        #     print(diff.total_seconds())
        #     print(diff)
        #     course_hours += diff.total_seconds()


        # course_hours /= 3600
        # print(course_hours)




        return CommandCode.SUCCESS

def setup(program) -> None:
    program.load_command(RegisterCourseCommand())
