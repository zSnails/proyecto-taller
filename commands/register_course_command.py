from typing import List
from command import Command, CommandCode
from models import Course, AccountRole, WeekDay
from datetime import datetime
from program import Program


class RegisterCourseCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "register-course"
        self.aliases = ["new-course", "nc"]
        self.required_role = AccountRole.ADMIN
        self.description = "Lets you register new courses"

    def run(self, ctx: Program) -> CommandCode:
        print("======= Registering a course =======")
        name = input("Course name> ")
        _credits = int(input("Course credits> "))

        _start_date = input("Start date (yyyy-mm-dd)> ")
        start_date = datetime.strptime(_start_date, "%Y-%m-%d")

        _end_date = input("End date (yyyy-mm-dd)> ")
        end_date = datetime.strptime(_end_date, "%Y-%m-%d")

        course_duration = end_date - start_date

        # TODO: add which career this belongs to (can belong to many careers)

        course_hours: float = 0.0
        weekly_hours: float = 0.0
        schedule = []
        print("=== Set schedule ===")
        while True:
            for idx, weekday in enumerate(WeekDay):
                print(idx + 1, str(weekday).split(".").pop())
            _day = input("Class day (enter day number) ('done' when finished)> ")
            if _day == "done":
                break
            _begin = input("Start hour (h:m:s)> ")
            _end = input("End hour (h:m:s)> ")

            day = WeekDay(int(_day))
            begin = datetime.strptime(_begin, "%H:%M:%S")
            end = datetime.strptime(_end, "%H:%M:%S")
            schedule.append((day, begin.time(), end.time()))
            weekly_hours += (end - begin).total_seconds() / 3600

        # course duration in hours
        course_hours = (course_duration.days // 30) * (weekly_hours * 4)

        available_careers: List[int] = []
        all_careers = ctx.manager.get_careers()
        for career in all_careers:
            print(career.id, career.name)
        while len(available_careers) != len(all_careers):
            to_register = input("Career availability ('done' when finished)> ")
            # TODO: manage unavailable careers

            if to_register.lower() == "done":
                break

            if to_register not in available_careers:
                available_careers.append(int(to_register))
            else:
                print("You already chose that career")

        course = Course(
            id=len(ctx.manager.courses) + 1,
            name=name,
            credits=_credits,
            course_hours=int(course_hours),
            start_date=start_date,
            end_date=end_date,
            schedule=schedule,
            belongs_to=available_careers,
            weekly_hours=int(weekly_hours),
        )

        ctx.manager.register_course(course)

        return CommandCode.SUCCESS


def setup(program) -> None:
    program.load_command(RegisterCourseCommand())
