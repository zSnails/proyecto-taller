from command import Command, CommandCode
from program import Program


class ChangeCourseStatusCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "update-course-status"
        self.aliases = ["ucs"]
        self.description = "Lets you change the status of a given course"

    def run(self, ctx: Program) -> CommandCode:
        print("====== Updating course status =======")
        user_courses = ctx.manager.get_account_courses(id=ctx.user.id)

        if not user_courses:
            print("You don't have any registered courses")
            return CommandCode.CONTINUE

        for course in user_courses:
            print(course.id, course.name)

        # TODO: toggle between passed or failed when one's already set
        _to_update = input("Enter course id ('cancel' to abort)> ")
        if _to_update.lower() == "cancel":
            return CommandCode.CONTINUE
        new_status = input("Enter new status> ")

        to_update = int(_to_update)

        ctx.manager.update_user_course_status(
            new_status, course_id=to_update, account_id=ctx.user.id
        )

        return CommandCode.SUCCESS


def setup(program):
    program.load_command(ChangeCourseStatusCommand())
