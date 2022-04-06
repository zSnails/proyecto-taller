from command import Command, CommandCode
from manager import Manager
from auth import Auth
from models import Account, AccountRole
from getpass import getpass
class RegisterCommand(Command):

    def __init__(self, manager = None, auth = None):
        super().__init__()
        self.name = "register-user"
        self.aliases = ["nu", "new-user"]
        self.manager: Manager = manager
        self.auth: Auth = auth
        self.required_role = AccountRole.ADMIN

    def run(self) -> CommandCode:
        print("==== Registering a new user ====")
        name = input("Please provide a name> ")
        if self.auth.check_existence(name):
            print("Username already in use")
            return CommandCode.CONTINUE

        usr = Account(
            id = len(self.manager.accounts) + 1,
            name = name,
            role = AccountRole(int(input(
                "Available roles: 1: STUDENT, 2: ADMIN\n"
                "What will this account be?> "))),
            career = 0
        )

        for career in self.manager.careers:
            print(career.id, ": ", career.name, sep="")

        usr.career = int(input("Please choose a career> "))

        for course in self.manager.get_courses(usr.career):
            print(course.id, ": ", course.name, sep="")

        # TODO: actually restrict the careers that you can register
        while len(usr.courses) != len(self.manager.courses):
            course_id = input("Enter course id (type 'done' when finished)> ")
            if course_id == 'done':
                break
            usr.courses.append(int(course_id))

        while True:
            passwd = getpass("Create a password> ")
            confirmation = getpass("Confirm your password> ")
            if passwd == confirmation: break
            else: print("The passwords don't match, please try again")

        self.manager.register_user(usr)
        self.auth.store_password(usr.name, passwd)
        return CommandCode.SUCCESS

def setup(program) -> None:
    program.load_command(RegisterCommand(manager=program.manager, auth=program.auth))
