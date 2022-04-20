from program import Program, CommandCode
from auth import Auth
from models import Account, AccountRole
from manager import Manager
from getpass import getpass
from os import listdir
from importlib import import_module
from json import JSONDecodeError

def register_admin_user(manager, auth):
    """
    Bloated function to register first user
    """
    print("==== Registering a new user ====")
    name = input("Please provide a name> ")

    usr = Account(
        id = len(manager.accounts) + 1,
        name = name,
        role = AccountRole.ADMIN,
        career = 0
    )

    for career in manager.careers:
        print(career.id, ": ", career.name, sep="")

    usr.career = int(input("Please choose a career> "))

    crs = manager.get_courses(usr.career)
    
    if crs:
        for course in crs:
            print(course.id, ": ", course.name, sep="")

        # TODO: actually restrict the careers that you can register
        while len(usr.courses) != len(manager.courses):
            course_id = input("Enter course id (type 'done' when finished)> ")
            if course_id == 'done': break

            usr.courses.append(int(course_id))

    while True:
        passwd = getpass("Create a password> ")
        confirmation = getpass("Confirm your password> ")
        if passwd == confirmation: break

        print("The passwords don't match, please try again")

    manager.register_user(usr)
    auth.store_password(usr.name, passwd)

def main():
    command_modules = listdir("./commands")
    # Manage system login
    manager = Manager()
    auth = Auth()
    try:
        auth.load_data()
    except JSONDecodeError:
        register_admin_user(manager, auth)
    
    
    is_valid = False
    
    while not is_valid:
        # username and password will live after this block
        username = input("Username> ")
        password = getpass("Password> ")
        is_valid = auth.verify_account(username, password)
    user_account = manager.get_account(name=username)
    p = Program(auth, manager, user_account)
    # load user commands
    for cmd in command_modules:
        if cmd in ('__init__.py', '__pycache__'): continue
        import_module(f"commands.{cmd[0:-3]}").setup(p)
    while True:
        code = p.prompt()
        if code == CommandCode.CONTINUE: continue
        elif code == CommandCode.EXIT: break
        elif code == CommandCode.NOT_FOUND:
            print("Command not found")
        elif code == CommandCode.FORBIDDEN:
            print("You can't use that command")

if __name__ == '__main__':
    main()