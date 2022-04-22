from command import Command, CommandCode
from program import Program

class ChangeCourseStatusCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "update-course-status"
        self.aliases = ["ucs"]

    def run(self, ctx: Program) -> CommandCode:
        print("====== Updating course status =======")
        user_courses = [course for course in ctx.manager.get_account_courses(id=ctx.user.id)]

        if not user_courses:
            print("You don't have any registered courses")
            return CommandCode.CONTINUE

        for course in user_courses:
            print(course.id, course.name)

        # TODO: toggle between passed or failed when one's already set        
        to_update = input("Enter course id ('cancel' to abort)> ")
        if to_update.lower() == 'cancel':
            return CommandCode.CONTINUE
        new_status = input("Enter new status> ")

        ctx.manager.update_user_course_status(new_status, course_id=to_update, account_id=ctx.user.id)

        return CommandCode.SUCCESS

def setup(program):
    program.load_command(ChangeCourseStatusCommand())
