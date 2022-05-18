from tkinter import Tk
from tkinter.ttk import Notebook
from users_tab import UsersTab
from careers_tab import CareersTab
from manager import Manager
from auth import Auth
from getpass import getpass
from models import Account, AccountRole
from register_root_modal import register_root_user_modal
from login_modal import login_modal
from json import JSONDecodeError
from program_gui import Program

def main():

    manager = Manager()
    auth = Auth()

    try:
        auth.load_data()
    except JSONDecodeError:
        register_root_user_modal(manager, auth)
        # register_admin_user(manager, auth)

    username = login_modal(auth)
    account = manager.get_account(name=username)
    
    p = Program(auth, manager, account, tabs=[CareersTab, UsersTab])
    p.run()
    # main_window = Tk()
    # main_window.wm_minsize(width=600, height=300)

    # tabs = Notebook(main_window)
    # tabs.add(UsersTab(), text="Users")
    # tabs.add(CareersTab(), text="Careers")




if __name__ == "__main__":
    main()
