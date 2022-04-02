from pickle import dump, load
from classes import Account
from getpass import getpass
from manager import Manager

auth_data = {}

with open("auth.pkl", "rb") as f:
    auth_data = load(f)
# NOTE: this isn't a good practice, but it gets the job done here, so I will be
# using this until I decide to change it to an actual password store
def store_password(username: str, password: str) -> None:
    """Helper function to store passwords in the password 'database'"""

    auth_data[username] = password

    with open("auth.pkl", "wb") as auth_file:
        dump(auth_data, auth_file)
        auth_file.close()
    with open("auth.pkl", "rb") as auth_file:
        auth_data = load(auth_file)

def verify_account(name: str, password: str) -> bool:
    """Helper function to verify valid login data"""

    if auth_data[name] == password:
        return True
    return False

# TODO: remove the login function and login directly from the manager
def login(manager: Manager) -> Account:
    """
    Sets the current logged user

    Parameters
    ----------
     - manager: a manager object

    Returns
    -------
     - An account instance
    """


    username = input("Username> ")
    password = getpass("Password> ")
    
    if verify_account(username, password):
        manager.set_current(username)

