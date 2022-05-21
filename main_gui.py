from tkinter import Tk
from tkinter.ttk import Notebook
from manager import Manager
from auth import Auth
from getpass import getpass
from models import Account, AccountRole
from register_root_modal import register_root_user_modal
from login_modal import login_modal
from json import JSONDecodeError
from program_gui import Program

# tabs
from users_tab import UsersTab
from careers_tab import CareersTab
from courses_tab import CoursesTab
from activities_tab import ActivitiesTab

def main():
    manager = Manager()
    auth = Auth()

    try:
        auth.load_data()
    except JSONDecodeError:
        register_root_user_modal(manager, auth)

    username = login_modal(auth)
    account = manager.get_account(name=username)

    p = Program(auth, manager, account, tabs=[CoursesTab, CareersTab, ActivitiesTab])
    p.run()


if __name__ == "__main__":
    main()
