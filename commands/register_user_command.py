from command import Command, CommandCode
from manager import Manager
from auth import Auth
from models import Account, AccountRole, ReportType
from getpass import getpass


class RegisterCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "register-user"
        self.aliases = ["nu", "new-user"]
        self.required_role = AccountRole.ADMIN
        self.description = "Starts the registration daemon"

    def run(self, ctx) -> CommandCode:
        print("==== Registering a new user ====")
        name = input("Please provide a name> ")
        if ctx.auth.check_existence(name):
            print("Username already in use")
            return CommandCode.CONTINUE

        usr = Account(
            id=len(ctx.manager.accounts) + 1,
            name=name,
            role=AccountRole(
                int(
                    input(
                        "Available roles: 1: STUDENT, 2: ADMIN\n"
                        "What will this account be?> "
                    )
                )
            ),
            career=0,
            reports=ReportType(
                int(
                    input(
                        "Available types: 1: DAILY, 2: WEEKLY\n" "Choose a report type>"
                    )
                )
            ),
            phone_number=input("Please provide a phone number (optional)> "),
        )

        for career in ctx.manager.careers:
            print(career.id, ": ", career.name, sep="")

        usr.career = int(input("Please choose a career> "))

        for course in ctx.manager.get_courses(usr.career):
            print(course.id, ": ", course.name, sep="")

        # TODO: actually restrict the careers that you can register
        while len(usr.courses) != len(ctx.manager.courses):
            course_id = input("Enter course id (type 'done' when finished)> ")
            if course_id == "done":
                break
            usr.courses.append(int(course_id))

        while True:
            passwd = getpass("Create a password> ")
            confirmation = getpass("Confirm your password> ")
            if passwd == confirmation:
                break
            else:
                print("The passwords don't match, please try again")

        ctx.manager.register_user(usr)
        ctx.auth.store_password(usr.name, passwd)
        return CommandCode.SUCCESS


def setup(program):
    program.load_command(RegisterCommand())
