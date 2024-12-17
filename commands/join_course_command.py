from typing import Callable
from command import Command, CommandCode
from models import Course
from program import Program


def course_filter(id: int) -> Callable[[Course], bool]:
    def the_filter(course: Course) -> bool:
        return course.id == id

    return the_filter


class JoinCourseCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "join-course"
        self.aliases = ["join"]
        self.description = "Lets you join a specific course"

    def run(self, ctx: Program) -> CommandCode:
        available_courses = [
            course
            for course in ctx.manager.get_courses(ctx.user.career)
            if course.id not in ctx.user.courses
        ]
        if not available_courses:
            print("There aren't any courses you can register right now")
            return CommandCode.CONTINUE

        for course in available_courses:
            print(course.id, course.name)

        _to_join = input("Course to join ('cancel' to abort)> ")

        if _to_join.lower() == "cancel":
            return CommandCode.CONTINUE

        to_join = int(_to_join)

        if to_join in ctx.user.courses:
            print("You already got that course!")
            return CommandCode.CONTINUE

        course_to_join: Course = list(
            filter(course_filter(to_join), available_courses)
        )[0]
        ctx.manager.update_account_courses(course_to_join, account_id=ctx.user.id)
        user = ctx.manager.get_account(id=ctx.user.id)
        if not user:
            return CommandCode.CONTINUE
        ctx.user = user
        return CommandCode.SUCCESS


def setup(program):
    program.load_command(JoinCourseCommand())
