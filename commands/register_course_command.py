from command import Command, CommandCode
from classes import Course, AccountRole

class RegisterCourse(Command):

    def __init__(self, manager = None):
        super().__init__()
        self.name = "register-course"
        self.aliases = ["new-course", "nc"]
        self.required_role = AccountRole.ADMIN
        self.manager = manager

    def run(self) -> CommandCode:
        c = Course(
            name = input("Course name> ")
        )
        return CommandCode.SUCCESS

def setup(program) -> None:
    program.load_command(RegisterCourse(manager=program.manager))
