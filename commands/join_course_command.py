from command import Command, CommandCode
from program import Program

class JoinCourseCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "join-course"
        self.aliases = ["join"]
        self.description = "Lets you join a specific course"

    def run(self, ctx: Program) -> CommandCode:
        available_courses = [course 
            for course in ctx.manager.get_courses(ctx.user.career)
             if course.id not in ctx.user.courses]
        if not available_courses:
            print("There aren't any courses you can register right now")
            return CommandCode.CONTINUE

        for course in available_courses:
            print(course.id, course.name)
        
        to_join = input("Course to join ('cancel' to abort)> ")

        if to_join.lower() == 'cancel':
            return CommandCode.CONTINUE

        to_join = int(to_join)

        if to_join in ctx.user.courses:
            print("You already got that course!")
            return CommandCode.CONTINUE

        ctx.manager.update_account_courses(to_join, account_id=ctx.user.id)
        ctx.user = ctx.manager.get_account(id=ctx.user.id)
        return CommandCode.SUCCESS

def setup(program):
    program.load_command(JoinCourseCommand())
