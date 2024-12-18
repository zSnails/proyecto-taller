from sys import stderr
from program import Program, CommandCode
from auth import Auth
from models import Account, AccountRole, ReportType
from manager import Manager
from getpass import getpass
from os import listdir
from importlib import import_module
from datetime import datetime, timedelta
from arrow import get
from colorama import Fore, Style


def register_admin_user(manager: Manager, auth: Auth) -> None:
    """
    The register admin user function allows the program to register the main
    administrator user

    Parameters
    ----------
        -   manager: A Manager class instance
        -   auth: An Auth class instance

    Returns
    -------
        -   None
    """
    print("==== Registering default user ====")
    name = input("Please provide a name> ")

    usr = Account(
        id=len(manager.accounts) + 1,
        name=name,
        role=AccountRole.ADMIN,
        career=0,
        courses=[],
        passed=[],
        failed=[],
        reports=ReportType.DAILY,
        activities=[],
    )

    while True:
        passwd = getpass("Create a password> ")
        confirmation = getpass("Confirm your password> ")
        if passwd == confirmation:
            break

        print("The passwords don't match, please try again")

    manager.register_user(usr)
    auth.store_password(usr.name, passwd)


def print_activities(activities, courses):
    """
    The print activities function allows the user to print daily activities

    Parameters
    ----------
        -   activities: A list of activities

    Returns
    -------
        -   None
    """
    print("Blue means leisure activity, Green means course bound activity")
    for activity in activities:
        day = get(activity.activity_date)

        end = datetime.strptime(str(activity.end_hour), "%H:%M:%S")
        begin = datetime.strptime(str(activity.start_hour), "%H:%M:%S")

        hours = round((end - begin).total_seconds() / 3600)

        col = Fore.BLUE

        if activity.course:
            col = Fore.GREEN

        print(
            f"\t- {col}{day.humanize()}{Style.RESET_ALL}: {activity.name}\n\t  Description: {activity.description}\n\t  Activity hours: {hours}"
        )
    from calendar import day_name

    print("===== Courses =======")
    for course in courses:
        print(f"[{course.id}] - {course.name}")
        for schedule in course.schedule:
            print(f"On: {day_name[schedule[0]-1]}\nAt: {schedule[1]}")


def main():
    """
    The main function is where the entry point of the program lives, this is where
    everything starts
    """
    command_modules = listdir("./commands")
    # Manage system login
    manager = Manager()
    auth = Auth()
    if not auth.load_data():
        register_admin_user(manager, auth)

    is_valid = False

    username = ""
    password = ""
    while not is_valid:
        # username and password will live after this block
        username = input("Username> ")
        password = getpass("Password> ")
        is_valid = auth.verify_account(username, password)
        if not is_valid:
            print("invalid credentials", file=stderr)

    user_account = manager.get_account(name=username)

    if not user_account:
        print("user_account is None", file=stderr)
        return

    program = Program(auth, manager, user_account)

    if datetime.today().weekday() == 0 and user_account.reports == ReportType.WEEKLY:
        monday = datetime.today()
        friday = monday + timedelta(days=5)
        activities = [
            activity
            for activity in manager.activities
            if monday.date() <= activity.activity_date
            and activity.activity_date <= friday.date()
            and activity.belongs_to == user_account.id
        ]
        courses = [course for course in manager.courses if course.id in user_account.courses]
        print("Weekly report - Activities for this week:")
        print_activities(activities, courses)

    elif user_account.reports == ReportType.DAILY:
        activities = [
            activity
            for activity in manager.activities
            if activity.activity_date == datetime.today().date()
            and activity.belongs_to == user_account.id
        ]
        courses = [
            course
            for course in manager.courses
            if course.schedule[0][0] == datetime.today().weekday() + 1
            and course.id in user_account.courses
        ]
        print("Daily report - Activities for today:")
        print_activities(activities, courses)

    # load user commands
    for cmd in command_modules:
        if cmd in ("__init__.py", "__pycache__"):
            continue
        import_module(f"commands.{cmd[0:-3]}").setup(program)

    print("Type 'help' for help")
    while True:
        code = program.prompt()
        if code == CommandCode.CONTINUE:
            continue
        elif code == CommandCode.EXIT:
            print("Thanks for using our software")
            break
        elif code == CommandCode.NOT_FOUND:
            print("Command not found")
        elif code == CommandCode.FORBIDDEN:
            print("You can't use that command")


if __name__ == "__main__":
    main()
